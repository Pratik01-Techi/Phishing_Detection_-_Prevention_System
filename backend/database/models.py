"""SQLAlchemy ORM models for PhishGuard."""
import json
import uuid
from datetime import datetime, timezone

from database.db import db


class ScanHistory(db.Model):
    __tablename__ = "scan_history"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_type = db.Column(db.String(10), nullable=False)  # url | email
    input_value = db.Column(db.Text, nullable=False)
    verdict = db.Column(db.String(20), nullable=False)
    risk_score = db.Column(db.Integer, default=0)
    confidence = db.Column(db.Float, default=0.0)
    features_json = db.Column(db.Text, default="{}")
    vt_result = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "scan_type": self.scan_type,
            "input_value": self.input_value[:200] if self.input_value else "",
            "verdict": self.verdict,
            "risk_score": self.risk_score,
            "confidence": self.confidence,
            "features": json.loads(self.features_json) if self.features_json else {},
            "vt_result": self.vt_result,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PhishingReport(db.Model):
    __tablename__ = "phishing_reports"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reported_url = db.Column(db.Text, nullable=False)
    report_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, default="")
    reporter_ip = db.Column(db.String(45), default="")
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "reported_url": self.reported_url,
            "report_type": self.report_type,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ModelMetrics(db.Model):
    __tablename__ = "model_metrics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    trained_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    dataset_size = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "trained_at": self.trained_at.isoformat() if self.trained_at else None,
            "dataset_size": self.dataset_size,
        }
