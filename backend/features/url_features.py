"""URL feature extraction — 18 features for ML phishing detection."""
import math
import re
import socket
from urllib.parse import urlparse

import tldextract
from fuzzywuzzy import fuzz

try:
    import whois
except ImportError:
    whois = None

from config import BRAND_NAMES, HIGH_RISK_TLDS, SUSPICIOUS_KEYWORDS


def _shannon_entropy(s: str) -> float:
    """Compute Shannon entropy of a string."""
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    length = len(s)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())


def _is_ip_address(domain: str) -> bool:
    """Check if domain is a raw IPv4 address."""
    try:
        socket.inet_aton(domain.split(":")[0])
        return True
    except OSError:
        return False


def _get_domain_age_days(domain: str) -> int:
    """Days since domain registration; -1 if unknown."""
    if not whois or not domain:
        return -1
    try:
        w = whois.whois(domain)
        created = w.creation_date
        if created is None:
            return -1
        if isinstance(created, list):
            created = created[0]
        from datetime import datetime, timezone
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return max(0, (now - created).days)
    except Exception:
        return -1


def _lookalike_score(domain: str) -> float:
    """Highest Levenshtein similarity to known brands (0.0–1.0)."""
    domain_lower = domain.lower().replace("www.", "")
    # Extract core domain without TLD for comparison
    parts = domain_lower.split(".")
    core = parts[0] if parts else domain_lower
    best = 0.0
    for brand in BRAND_NAMES:
        ratio = fuzz.ratio(core, brand) / 100.0
        if ratio > best:
            best = ratio
        # Also check if brand appears as substring with typos
        partial = fuzz.partial_ratio(core, brand) / 100.0
        if partial > best and len(core) >= 4:
            best = partial
    return round(best, 4)


def extract_url_features(url: str, skip_whois: bool = False) -> dict:
    """
    Extract 18 URL features for ML model input.
    Returns dict with all feature names and values.
    """
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    full_url = url
    domain = parsed.netloc or ""
    path_query = (parsed.path or "") + (parsed.query or "")

    ext = tldextract.extract(url)
    registered_domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    subdomain_parts = [p for p in ext.subdomain.split(".") if p] if ext.subdomain else []

    # Feature 1–7: basic counts
    url_length = len(full_url)
    domain_length = len(domain)
    num_dots = full_url.count(".")
    num_hyphens = full_url.count("-")
    num_underscores = full_url.count("_")
    num_slashes = full_url.count("/")
    num_at_symbol = 1 if "@" in full_url else 0

    # Feature 8: double slash after protocol (suspicious redirect trick)
    scheme_end = full_url.find("://")
    after_proto = full_url[scheme_end + 3:] if scheme_end >= 0 else full_url
    num_double_slash = 1 if "//" in after_proto else 0

    # Feature 9–11
    has_ip_address = 1 if _is_ip_address(domain.split(":")[0]) else 0
    is_https = 1 if parsed.scheme == "https" else 0
    subdomain_depth = len(subdomain_parts)

    # Feature 12: suspicious keywords
    url_lower = full_url.lower()
    suspicious_keywords = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)

    # Feature 13: domain age
    lookup_domain = registered_domain or domain
    domain_age_days = -1 if skip_whois else _get_domain_age_days(lookup_domain)

    # Feature 14: TLD risk
    tld = f".{ext.suffix}" if ext.suffix else ""
    tld_risk_score = 1 if tld.lower() in HIGH_RISK_TLDS else 0

    # Feature 15–17
    url_entropy = round(_shannon_entropy(full_url), 4)
    digits = sum(1 for c in full_url if c.isdigit())
    digit_ratio = round(digits / url_length, 4) if url_length > 0 else 0.0
    special_chars = "%=?&#"
    special_char_count = sum(full_url.count(c) for c in special_chars)

    # Feature 18: lookalike
    lookalike = _lookalike_score(domain)

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "num_dots": num_dots,
        "num_hyphens": num_hyphens,
        "num_underscores": num_underscores,
        "num_slashes": num_slashes,
        "num_at_symbol": num_at_symbol,
        "num_double_slash": num_double_slash,
        "has_ip_address": has_ip_address,
        "is_https": is_https,
        "subdomain_depth": subdomain_depth,
        "suspicious_keywords": suspicious_keywords,
        "domain_age_days": domain_age_days,
        "tld_risk_score": tld_risk_score,
        "url_entropy": url_entropy,
        "digit_ratio": digit_ratio,
        "special_char_count": special_char_count,
        "lookalike_score": lookalike,
    }


FEATURE_NAMES = [
    "url_length", "domain_length", "num_dots", "num_hyphens", "num_underscores",
    "num_slashes", "num_at_symbol", "num_double_slash", "has_ip_address", "is_https",
    "subdomain_depth", "suspicious_keywords", "domain_age_days", "tld_risk_score",
    "url_entropy", "digit_ratio", "special_char_count", "lookalike_score",
]


def features_to_vector(features: dict) -> list:
    """Convert feature dict to ordered list for ML model."""
    return [features.get(name, 0) for name in FEATURE_NAMES]


def get_triggered_rules(features: dict) -> list:
    """Rule-based flags explaining why a URL looks suspicious."""
    rules = []
    if features.get("has_ip_address"):
        rules.append("ip_address_domain")
    if features.get("suspicious_keywords", 0) >= 2:
        rules.append("suspicious_keywords")
    elif features.get("suspicious_keywords", 0) >= 1:
        rules.append("suspicious_keyword")
    if features.get("tld_risk_score"):
        rules.append("high_risk_tld")
    if features.get("domain_age_days", -1) >= 0 and features["domain_age_days"] < 30:
        rules.append("new_domain")
    if features.get("lookalike_score", 0) >= 0.75:
        rules.append("brand_lookalike")
    if features.get("num_at_symbol"):
        rules.append("at_symbol_redirect")
    if features.get("num_double_slash"):
        rules.append("double_slash_trick")
    if not features.get("is_https"):
        rules.append("no_https")
    if features.get("subdomain_depth", 0) >= 3:
        rules.append("deep_subdomain")
    if features.get("url_length", 0) > 100:
        rules.append("excessive_url_length")
    return rules
