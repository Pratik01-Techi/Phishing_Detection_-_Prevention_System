"""PhishGuard — Main Flask REST API."""
import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Ensure backend root is on path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from config import MODEL_PATH, PHISHING_THRESHOLD, SUSPICIOUS_THRESHOLD
from database.db import db, init_db
from database.models import ModelMetrics, PhishingReport, ScanHistory
from features.email_features import analyze_email
from features.url_features import extract_url_features, get_triggered_rules
from models.ml_model import load_and_train, load_model, predict_url
from services.virustotal import check_url as vt_check_url, is_connected as vt_connected
from services.whois_service import get_domain_age

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "phishguard-dev")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", f"sqlite:///{BACKEND_DIR / 'phishguard.db'}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, resources={r"/api/*": {"origins": "*"}})

init_db(app)

# Global model bundle
_model_bundle = None


def get_model():
    global _model_bundle
    if _model_bundle is None:
        _model_bundle = load_model()
        if _model_bundle is None:
            logger.info("No model found — training synthetic model...")
            metrics = load_and_train()
            _model_bundle = load_model()
            if _model_bundle and metrics:
                with app.app_context():
                    m = ModelMetrics(
                        accuracy=metrics.get("accuracy"),
                        precision=metrics.get("precision"),
                        recall=metrics.get("recall"),
                        f1_score=metrics.get("f1_score"),
                        dataset_size=metrics.get("dataset_size"),
                    )
                    db.session.add(m)
                    db.session.commit()
    return _model_bundle


def _combine_verdict(ml_verdict: str, vt_verdict: str, rules: list, ml_conf: float) -> tuple:
    """Combine ML, VT, and rules into final verdict and risk score."""
    risk = int(ml_conf * 100)

    if vt_verdict == "MALICIOUS":
        risk = max(risk, 85)
    elif vt_verdict == "SUSPICIOUS":
        risk = max(risk, 60)

    risk += len(rules) * 5
    risk = min(100, risk)

    if ml_verdict == "PHISHING" or vt_verdict == "MALICIOUS" or risk >= 70:
        return "PHISHING", risk
    if ml_verdict == "SUSPICIOUS" or vt_verdict == "SUSPICIOUS" or risk >= 40:
        return "SUSPICIOUS", risk
    return "CLEAN", risk


def _format_domain_age(days: int) -> str:
    if days < 0:
        return "Unknown"
    if days == 1:
        return "1 day"
    return f"{days} days"


@app.route("/api/health", methods=["GET"])
def health():
    model = get_model()
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "vt_api": "connected" if vt_connected() else "not_configured",
    })


@app.route("/api/analyze/url", methods=["POST"])
def analyze_url():
    try:
        data = request.get_json() or {}
        url = (data.get("url") or "").strip()
        if not url:
            return jsonify({"error": "URL is required"}), 400

        scan_id = str(uuid.uuid4())
        features = extract_url_features(url)
        rules = get_triggered_rules(features)

        model = get_model()
        ml_result = predict_url(url, model)
        ml_verdict = ml_result["verdict"]
        confidence = ml_result["confidence"]

        # VirusTotal (optional)
        vt_result = vt_check_url(url)
        vt_verdict = vt_result["verdict"]

        # Domain age
        import tldextract
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
        whois_info = get_domain_age(domain)
        if whois_info["age_days"] >= 0:
            features["domain_age_days"] = whois_info["age_days"]
            if whois_info["age_days"] < 30:
                if "new_domain" not in rules:
                    rules.append("new_domain")

        verdict, risk_score = _combine_verdict(ml_verdict, vt_verdict, rules, confidence)

        # Log scan
        with app.app_context():
            scan = ScanHistory(
                id=scan_id,
                scan_type="url",
                input_value=url[:500],
                verdict=verdict,
                risk_score=risk_score,
                confidence=confidence,
                features_json=json.dumps(features),
                vt_result=vt_result.get("detections", "N/A"),
            )
            db.session.add(scan)
            db.session.commit()

        return jsonify({
            "scan_id": scan_id,
            "verdict": verdict,
            "confidence": round(confidence * 100, 1) if confidence <= 1 else confidence,
            "risk_score": risk_score,
            "ml_verdict": ml_verdict,
            "vt_verdict": vt_verdict,
            "features": features,
            "triggered_rules": rules,
            "domain_age": whois_info.get("age_display", _format_domain_age(features.get("domain_age_days", -1))),
            "vt_detections": vt_result.get("detections", "N/A"),
            "feature_importances": ml_result.get("feature_importances", {}),
        })
    except Exception as e:
        logger.exception("URL analysis error")
        return jsonify({"error": str(e)}), 500


@app.route("/api/analyze/email", methods=["POST"])
def analyze_email_endpoint():
    try:
        data = request.get_json() or {}
        email_text = (data.get("email_text") or "").strip()
        if not email_text:
            return jsonify({"error": "email_text is required"}), 400

        result = analyze_email(email_text)
        scan_id = str(uuid.uuid4())

        with app.app_context():
            scan = ScanHistory(
                id=scan_id,
                scan_type="email",
                input_value=email_text[:200],
                verdict=result["verdict"],
                risk_score=result["risk_score"],
                confidence=result["risk_score"] / 100.0,
                features_json=json.dumps({
                    "spf": result["spf"],
                    "dkim": result["dkim"],
                    "dmarc": result["dmarc"],
                }),
            )
            db.session.add(scan)
            db.session.commit()

        return jsonify({
            "scan_id": scan_id,
            "verdict": result["verdict"],
            "risk_score": result["risk_score"],
            "spf": result["spf"],
            "dkim": result["dkim"],
            "dmarc": result["dmarc"],
            "triggered_rules": result["triggered_rules"],
            "suspicious_links": result["suspicious_links"],
            "urgency_score": result["urgency_score"],
        })
    except Exception as e:
        logger.exception("Email analysis error")
        return jsonify({"error": str(e)}), 500


@app.route("/api/report", methods=["POST"])
def submit_report():
    try:
        data = request.get_json() or {}
        url = (data.get("url") or "").strip()
        report_type = (data.get("type") or "phishing").strip()
        description = (data.get("description") or "").strip()

        if not url:
            return jsonify({"error": "url is required"}), 400

        report_id = str(uuid.uuid4())
        reporter_ip = request.remote_addr or ""

        with app.app_context():
            report = PhishingReport(
                id=report_id,
                reported_url=url,
                report_type=report_type,
                description=description,
                reporter_ip=reporter_ip,
            )
            db.session.add(report)
            db.session.commit()

        return jsonify({"report_id": report_id, "status": "received"}), 201
    except Exception as e:
        logger.exception("Report submission error")
        return jsonify({"error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    try:
        limit = min(int(request.args.get("limit", 50)), 100)
        with app.app_context():
            scans = (
                ScanHistory.query
                .order_by(ScanHistory.created_at.desc())
                .limit(limit)
                .all()
            )
        return jsonify([s.to_dict() for s in scans])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        with app.app_context():
            total = ScanHistory.query.count()
            phishing = ScanHistory.query.filter_by(verdict="PHISHING").count()
            clean = ScanHistory.query.filter_by(verdict="CLEAN").count()
            suspicious = ScanHistory.query.filter_by(verdict="SUSPICIOUS").count()

            today_start = datetime.now(timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            scans_today = ScanHistory.query.filter(
                ScanHistory.created_at >= today_start
            ).count()

            # Top TLDs from URL scans
            url_scans = ScanHistory.query.filter_by(scan_type="url").limit(500).all()
            tld_counts = {}
            import tldextract
            for s in url_scans:
                try:
                    ext = tldextract.extract(s.input_value)
                    tld = f".{ext.suffix}" if ext.suffix else "unknown"
                    tld_counts[tld] = tld_counts.get(tld, 0) + 1
                except Exception:
                    pass
            top_tlds = sorted(tld_counts.items(), key=lambda x: -x[1])[:5]
            top_tlds = [{"tld": t, "count": c} for t, c in top_tlds]

            detection_rate = (
                f"{((phishing + suspicious) / total * 100):.1f}%"
                if total > 0 else "0%"
            )

        return jsonify({
            "total_scans": total,
            "phishing_detected": phishing,
            "clean_urls": clean,
            "suspicious": suspicious,
            "detection_rate": detection_rate,
            "top_tlds": top_tlds,
            "scans_today": scans_today,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    get_model()  # Ensure model is loaded/trained on startup
    app.run(host="0.0.0.0", port=5000, debug=True)
