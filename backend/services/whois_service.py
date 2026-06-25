"""WhoisXML API integration with python-whois fallback."""
import logging

import requests

from config import WHOISXML_API_KEY

logger = logging.getLogger(__name__)

try:
    import whois as python_whois
except ImportError:
    python_whois = None


def get_domain_age(domain: str) -> dict:
    """
    Get domain registration info.
    Returns age_days, formatted age string, registrar.
    """
    if WHOISXML_API_KEY:
        try:
            resp = requests.get(
                "https://www.whoisxmlapi.com/whoisserver/WhoisService",
                params={
                    "apiKey": WHOISXML_API_KEY,
                    "domainName": domain,
                    "outputFormat": "JSON",
                },
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                created = (
                    data.get("WhoisRecord", {})
                    .get("createdDate")
                    or data.get("WhoisRecord", {}).get("registryData", {}).get("createdDate")
                )
                if created:
                    from datetime import datetime, timezone
                    try:
                        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                        days = (datetime.now(timezone.utc) - dt).days
                        return {
                            "age_days": days,
                            "age_display": _format_age(days),
                            "source": "whoisxml",
                        }
                    except Exception:
                        pass
        except Exception as e:
            logger.warning("WhoisXML API error: %s", e)

    # Fallback to python-whois
    if python_whois:
        try:
            w = python_whois.whois(domain)
            created = w.creation_date
            if created:
                if isinstance(created, list):
                    created = created[0]
                from datetime import datetime, timezone
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
                days = (datetime.now(timezone.utc) - created).days
                return {
                    "age_days": days,
                    "age_display": _format_age(days),
                    "source": "python-whois",
                }
        except Exception:
            pass

    return {"age_days": -1, "age_display": "Unknown", "source": "none"}


def _format_age(days: int) -> str:
    if days < 0:
        return "Unknown"
    if days == 0:
        return "Today"
    if days == 1:
        return "1 day"
    if days < 30:
        return f"{days} days"
    if days < 365:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''}"
    years = days // 365
    return f"{years} year{'s' if years > 1 else ''}"
