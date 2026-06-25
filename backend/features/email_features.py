"""Email header and body analysis for phishing detection."""
import re
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from config import BRAND_NAMES, URGENCY_KEYWORDS

RISKY_EXTENSIONS = {".exe", ".zip", ".js", ".vbs", ".bat", ".scr", ".cmd", ".msi"}


def _parse_email(raw: str) -> tuple:
    """Parse raw email text into message object and body."""
    try:
        msg = BytesParser(policy=policy.default).parsebytes(raw.encode("utf-8", errors="replace"))
    except Exception:
        msg = BytesParser(policy=policy.default).parsebytes(
            ("From: unknown\n\n" + raw).encode("utf-8")
        )
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/html":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="replace")
                    break
            elif ctype == "text/plain" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode("utf-8", errors="replace")
        else:
            body = str(msg.get_payload() or "")
    return msg, body


def _header_auth(msg, header_prefix: str) -> str:
    """Extract SPF/DKIM/DMARC result from Authentication-Results or dedicated headers."""
    auth_results = msg.get_all("Authentication-Results", [])
    for ar in auth_results:
        ar_lower = ar.lower()
        if header_prefix == "spf" and "spf=" in ar_lower:
            m = re.search(r"spf=(\w+)", ar_lower)
            if m:
                return m.group(1).upper()
        if header_prefix == "dkim" and "dkim=" in ar_lower:
            m = re.search(r"dkim=(\w+)", ar_lower)
            if m:
                return m.group(1).upper()
        if header_prefix == "dmarc" and "dmarc=" in ar_lower:
            m = re.search(r"dmarc=(\w+)", ar_lower)
            if m:
                return m.group(1).upper()

    # Fallback dedicated headers
    dedicated = {
        "spf": ["Received-SPF", "X-SPF-Result"],
        "dkim": ["DKIM-Signature"],
        "dmarc": ["X-DMARC-Result"],
    }
    for h in dedicated.get(header_prefix, []):
        val = msg.get(h)
        if val:
            val_lower = val.lower()
            if "pass" in val_lower:
                return "PASS"
            if "fail" in val_lower:
                return "FAIL"
            if header_prefix == "dkim" and "v=1" in val_lower:
                return "PASS"
    return "MISSING"


def _extract_email_address(header_val: str) -> tuple:
    """Return (display_name, email_address) from From/Reply-To header."""
    if not header_val:
        return "", ""
    m = re.match(r'^"?([^"<]*)"?\s*<?([^>]+@[^>]+)>?', header_val.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip().lower()
    if "@" in header_val:
        return "", header_val.strip().lower()
    return header_val, ""


def _domain_from_email(email: str) -> str:
    if "@" in email:
        return email.split("@")[-1].lower()
    return ""


def analyze_email(email_text: str) -> dict:
    """
    Analyze raw email content.
    Returns risk_score (0-100), triggered_rules, and detail fields.
    """
    msg, body = _parse_email(email_text)
    triggered_rules = []
    risk_points = 0

    # 1–3: SPF, DKIM, DMARC
    spf = _header_auth(msg, "spf")
    dkim = _header_auth(msg, "dkim")
    dmarc = _header_auth(msg, "dmarc")

    if spf == "FAIL":
        triggered_rules.append("spf_fail")
        risk_points += 15
    elif spf == "MISSING":
        triggered_rules.append("spf_missing")
        risk_points += 8

    if dkim == "FAIL":
        triggered_rules.append("dkim_fail")
        risk_points += 15
    elif dkim == "MISSING":
        triggered_rules.append("dkim_missing")
        risk_points += 8

    if dmarc == "FAIL":
        triggered_rules.append("dmarc_fail")
        risk_points += 15
    elif dmarc == "MISSING":
        triggered_rules.append("dmarc_missing")
        risk_points += 5

    # 4: From vs Reply-To domain mismatch
    from_header = msg.get("From", "")
    reply_header = msg.get("Reply-To", "")
    _, from_email = _extract_email_address(from_header)
    _, reply_email = _extract_email_address(reply_header)
    from_domain = _domain_from_email(from_email)
    reply_domain = _domain_from_email(reply_email)
    domain_mismatch = bool(
        reply_domain and from_domain and reply_domain != from_domain
    )
    if domain_mismatch:
        triggered_rules.append("reply_to_mismatch")
        risk_points += 20

    # 5: Display name spoofing
    display_name, _ = _extract_email_address(from_header)
    display_spoofing = False
    if display_name:
        dn_lower = display_name.lower()
        for brand in BRAND_NAMES:
            if brand in dn_lower and brand not in from_domain:
                display_spoofing = True
                triggered_rules.append("display_name_spoofing")
                risk_points += 25
                break

    # 6: Urgency keywords
    full_text = (email_text + " " + body).lower()
    urgency_count = sum(1 for kw in URGENCY_KEYWORDS if kw in full_text)
    if urgency_count >= 3:
        triggered_rules.append("high_urgency_language")
        risk_points += 20
    elif urgency_count >= 1:
        triggered_rules.append("urgency_language")
        risk_points += 10

    # 7–8: Links in body
    links = re.findall(r'https?://[^\s<>"\']+', body + email_text)
    link_count = len(links)
    external_domains = set()
    for link in links:
        try:
            dom = urlparse(link).netloc.lower()
            if dom and dom != from_domain:
                external_domains.add(dom)
        except Exception:
            pass
    external_count = len(external_domains)

    if link_count >= 5:
        triggered_rules.append("many_links")
        risk_points += 10
    if external_count >= 3:
        triggered_rules.append("multiple_external_domains")
        risk_points += 15

    # 9: HTML obfuscation
    html_obfuscation = False
    if "<" in body:
        try:
            soup = BeautifulSoup(body, "html.parser")
            for tag in soup.find_all(style=True):
                style = tag.get("style", "").lower()
                if "display:none" in style.replace(" ", "") or "font-size:0" in style or "font-size: 0" in style:
                    html_obfuscation = True
                    break
            for tag in soup.find_all(font=True):
                size = tag.get("size")
                if size and str(size) in ("0", "1"):
                    html_obfuscation = True
                    break
        except Exception:
            pass
    if html_obfuscation:
        triggered_rules.append("html_obfuscation")
        risk_points += 20

    # 10: Attachment risk
    attachment_risk = False
    for part in msg.walk():
        filename = part.get_filename()
        if filename:
            ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            if ext in RISKY_EXTENSIONS:
                attachment_risk = True
                triggered_rules.append("risky_attachment")
                risk_points += 30
                break

    risk_score = min(100, risk_points)

    # Verdict from risk score
    if risk_score >= 60:
        verdict = "PHISHING"
    elif risk_score >= 35:
        verdict = "SUSPICIOUS"
    else:
        verdict = "CLEAN"

    suspicious_links = list(links)[:10]

    return {
        "verdict": verdict,
        "risk_score": risk_score,
        "spf": spf,
        "dkim": dkim,
        "dmarc": dmarc,
        "from_domain_mismatch": domain_mismatch,
        "display_name_spoofing": display_spoofing,
        "urgency_score": urgency_count,
        "link_count": link_count,
        "external_domain_count": external_count,
        "html_obfuscation": html_obfuscation,
        "attachment_risk": attachment_risk,
        "triggered_rules": triggered_rules,
        "suspicious_links": suspicious_links,
    }
