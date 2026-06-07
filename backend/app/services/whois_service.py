from typing import Optional
import whois
from app.config import settings


async def get_whois_info(domain: str) -> dict:
    result = {
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "updated_date": None,
        "name_servers": [],
        "registrar_abuse_contact": None,
        "dnssec": False,
        "raw": None
    }

    try:
        w = whois.whois(domain, timeout=settings.WHOIS_TIMEOUT)

        if w.registrar:
            result["registrar"] = str(w.registrar)

        if w.creation_date:
            dates = w.creation_date
            if isinstance(dates, list):
                result["creation_date"] = str(dates[0])
            else:
                result["creation_date"] = str(dates)

        if w.expiration_date:
            dates = w.expiration_date
            if isinstance(dates, list):
                result["expiration_date"] = str(dates[0])
            else:
                result["expiration_date"] = str(dates)

        if w.updated_date:
            dates = w.updated_date
            if isinstance(dates, list):
                result["updated_date"] = str(dates[0])
            else:
                result["updated_date"] = str(dates)

        if w.name_servers:
            if isinstance(w.name_servers, list):
                result["name_servers"] = [str(ns).rstrip(".") for ns in w.name_servers]
            else:
                result["name_servers"] = [str(w.name_servers).rstrip(".")]

        if hasattr(w, "dnssec") and w.dnssec:
            result["dnssec"] = True

        if w.emails:
            if isinstance(w.emails, list):
                result["registrar_abuse_contact"] = str(w.emails[0])
            else:
                result["registrar_abuse_contact"] = str(w.emails)

        result["raw"] = w.text[:2000] if w.text else None

    except Exception:
        result["registrar"] = "Information unavailable"
        result["creation_date"] = "Unknown"

    return result
