"""VirusTotal v3 API integration with graceful fallback."""
import base64
import logging

import requests

from config import VIRUSTOTAL_API_KEY

logger = logging.getLogger(__name__)
VT_BASE = "https://www.virustotal.com/api/v3"


def check_url(url: str) -> dict:
    """
    Scan URL via VirusTotal. Returns verdict and detection stats.
    Falls back to unknown if API key missing or request fails.
    """
    if not VIRUSTOTAL_API_KEY:
        return {
            "verdict": "UNKNOWN",
            "detections": "N/A",
            "malicious": 0,
            "total": 0,
            "connected": False,
        }

    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    try:
        # Try existing analysis first
        resp = requests.get(
            f"{VT_BASE}/urls/{url_id}",
            headers=headers,
            timeout=15,
        )
        if resp.status_code == 404:
            # Submit for analysis
            submit = requests.post(
                f"{VT_BASE}/urls",
                headers=headers,
                data={"url": url},
                timeout=15,
            )
            if submit.status_code in (200, 201):
                analysis_id = submit.json().get("data", {}).get("id")
                if analysis_id:
                    resp = requests.get(
                        f"{VT_BASE}/analyses/{analysis_id}",
                        headers=headers,
                        timeout=15,
                    )
            else:
                return _fallback()

        if resp.status_code != 200:
            return _fallback()

        data = resp.json().get("data", {})
        attrs = data.get("attributes", {})
        stats = attrs.get("last_analysis_stats", attrs.get("stats", {}))
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        total = sum(stats.values()) if stats else 0
        flagged = malicious + suspicious

        if malicious >= 3:
            verdict = "MALICIOUS"
        elif flagged >= 1:
            verdict = "SUSPICIOUS"
        else:
            verdict = "CLEAN"

        return {
            "verdict": verdict,
            "detections": f"{flagged}/{total} engines" if total else "0/0 engines",
            "malicious": malicious,
            "total": total,
            "connected": True,
        }
    except Exception as e:
        logger.warning("VirusTotal API error: %s", e)
        return _fallback()


def _fallback():
    return {
        "verdict": "UNKNOWN",
        "detections": "N/A",
        "malicious": 0,
        "total": 0,
        "connected": False,
    }


def is_connected() -> bool:
    """Check if VT API key is configured."""
    return bool(VIRUSTOTAL_API_KEY)
