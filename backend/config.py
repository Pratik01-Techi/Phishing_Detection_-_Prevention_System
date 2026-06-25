"""PhishGuard configuration — loads from environment with safe defaults."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "phishing_model.pkl"
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_PATH = DATA_DIR / "training_data.csv"

# API keys (optional — app falls back to ML-only mode)
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
WHOISXML_API_KEY = os.getenv("WHOISXML_API_KEY", "")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "phishguard-dev-secret-change-in-prod")
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'phishguard.db'}")

# Verdict thresholds
PHISHING_THRESHOLD = 0.65
SUSPICIOUS_THRESHOLD = 0.40

# High-risk TLDs
HIGH_RISK_TLDS = {".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club", ".online"}

# Brand list for lookalike detection
BRAND_NAMES = [
    "google", "paypal", "amazon", "facebook", "apple", "microsoft",
    "netflix", "instagram", "twitter", "linkedin", "bankofamerica",
    "wellsfargo", "chase", "dropbox", "adobe", "steam", "github",
    "yahoo", "ebay", "spotify",
]

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "bank", "confirm",
    "password", "signin", "ebayisapi", "webscr", "paypal",
]

URGENCY_KEYWORDS = [
    "urgent", "immediately", "suspended", "verify now", "click here",
    "act now", "expires", "limited time", "confirm your", "unusual activity",
]
