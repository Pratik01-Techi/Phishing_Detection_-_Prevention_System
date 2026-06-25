"""ML training and prediction — Random Forest + Gradient Boosting ensemble."""
import os
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import MODEL_PATH, SAMPLE_DATA_PATH, PHISHING_THRESHOLD, SUSPICIOUS_THRESHOLD
from features.url_features import FEATURE_NAMES, extract_url_features, features_to_vector


def _generate_synthetic_data(n_samples: int = 800) -> pd.DataFrame:
    """Generate synthetic phishing/clean URLs for first-run training."""
    clean_urls = [
        "https://github.com/user/repo",
        "https://google.com/search?q=test",
        "https://stackoverflow.com/questions/123",
        "https://amazon.com/product/12345",
        "https://microsoft.com/en-us",
        "https://linkedin.com/in/profile",
        "https://netflix.com/browse",
        "https://apple.com/iphone",
        "https://wikipedia.org/wiki/Main",
        "https://reddit.com/r/programming",
        "https://youtube.com/watch?v=abc",
        "https://twitter.com/home",
        "https://dropbox.com/home",
        "https://adobe.com/products",
        "https://spotify.com/account",
    ]
    phishing_templates = [
        "http://paypa1-secure-verify.tk/login/confirm?id={}",
        "http://192.168.1.{}/amazon-account-suspended",
        "https://google-security-alert.000webhostapp.com/verify",
        "http://secure-login-{0}.ml/account/update",
        "http://bankofamerica-verify.ga/signin?user={}",
        "http://apple-id-locked.cf/restore?token={}",
        "http://microsoft-account-update.xyz/login",
        "http://netflix-billing-suspended.tk/payment",
        "http://facebook-security-check.online/confirm",
        "http://chase-online-banking.ml/verify",
        "http://wellsfargo-alert.top/account",
        "http://dropbox-share-document.ga/download",
        "http://paypal-resolution-center.tk/confirm",
        "http://amazon-prime-renewal.cf/billing",
        "http://instagram-verify-badge.online/claim",
    ]

    rows = []
    for url in clean_urls:
        rows.append({"url": url, "label": 0})
        for i in range(8):
            rows.append({"url": url + f"?ref={i}", "label": 0})

    for tmpl in phishing_templates:
        for i in range(25):
            rows.append({"url": tmpl.format(i, i), "label": 1})

    # Add noise variations
    random.shuffle(rows)
    return pd.DataFrame(rows[:n_samples])


def load_and_train(csv_path: str = None) -> dict:
    """
    Load dataset (or generate synthetic), train ensemble, save model.
    Returns metrics dict.
    """
    path = csv_path or str(SAMPLE_DATA_PATH)
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "label" not in df.columns:
            df["label"] = df.get("Label", df.get("class", 0))
        if "url" not in df.columns:
            df["url"] = df.get("URL", df.iloc[:, 0])
    else:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        df = _generate_synthetic_data()
        df.to_csv(path, index=False)

    X, y = [], []
    for _, row in df.iterrows():
        try:
            feats = extract_url_features(str(row["url"]), skip_whois=True)
            X.append(features_to_vector(feats))
            y.append(int(row["label"]))
        except Exception:
            continue

    X = np.array(X)
    y = np.array(y)

    if len(X) < 20:
        df = _generate_synthetic_data(500)
        X, y = [], []
        for _, row in df.iterrows():
            feats = extract_url_features(str(row["url"]), skip_whois=True)
            X.append(features_to_vector(feats))
            y.append(int(row["label"]))
        X = np.array(X)
        y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
    )

    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    gb.fit(X_train, y_train)

    # Ensemble: weighted average (RF 0.6, GB 0.4)
    rf_proba = rf.predict_proba(X_test)[:, 1]
    gb_proba = gb.predict_proba(X_test)[:, 1]
    ensemble_proba = 0.6 * rf_proba + 0.4 * gb_proba
    y_pred = (ensemble_proba >= 0.5).astype(int)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
        "f1_score": round(f1_score(y_test, y_pred, zero_division=0), 4),
        "dataset_size": len(X),
    }

    model_bundle = {
        "rf": rf,
        "gb": gb,
        "feature_names": FEATURE_NAMES,
        "weights": (0.6, 0.4),
        "metrics": metrics,
    }

    os.makedirs(MODEL_PATH.parent, exist_ok=True)
    joblib.dump(model_bundle, MODEL_PATH)
    return metrics


def load_model():
    """Load trained model bundle from disk."""
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


def predict_url(url: str, model_bundle: dict = None) -> dict:
    """
    Predict phishing probability for a URL.
    Returns verdict, confidence, feature_importances.
    """
    if model_bundle is None:
        model_bundle = load_model()
    if model_bundle is None:
        # Untrained fallback: rule-based only
        feats = extract_url_features(url)
        score = _rule_based_score(feats)
        return {
            "verdict": _score_to_verdict(score),
            "confidence": score,
            "phishing_probability": score,
            "feature_importances": {},
        }

    feats = extract_url_features(url)
    X = np.array([features_to_vector(feats)])

    rf = model_bundle["rf"]
    gb = model_bundle["gb"]
    w_rf, w_gb = model_bundle["weights"]

    rf_proba = rf.predict_proba(X)[0][1]
    gb_proba = gb.predict_proba(X)[0][1]
    prob = w_rf * rf_proba + w_gb * gb_proba
    confidence = round(float(prob), 4)

    verdict = _score_to_verdict(confidence)

    # Feature importances from RF
    importances = dict(zip(FEATURE_NAMES, rf.feature_importances_.tolist()))
    top_importances = dict(sorted(importances.items(), key=lambda x: -x[1])[:5])

    return {
        "verdict": verdict,
        "confidence": confidence,
        "phishing_probability": confidence,
        "feature_importances": top_importances,
    }


def _score_to_verdict(score: float) -> str:
    if score >= PHISHING_THRESHOLD:
        return "PHISHING"
    if score >= SUSPICIOUS_THRESHOLD:
        return "SUSPICIOUS"
    return "CLEAN"


def _rule_based_score(feats: dict) -> float:
    """Fallback score when no ML model is loaded."""
    score = 0.0
    if feats.get("has_ip_address"):
        score += 0.25
    if feats.get("tld_risk_score"):
        score += 0.2
    if feats.get("suspicious_keywords", 0) >= 2:
        score += 0.25
    elif feats.get("suspicious_keywords", 0) >= 1:
        score += 0.1
    if feats.get("lookalike_score", 0) >= 0.75:
        score += 0.25
    if feats.get("domain_age_days", -1) >= 0 and feats["domain_age_days"] < 30:
        score += 0.15
    if not feats.get("is_https"):
        score += 0.05
    return min(1.0, score)
