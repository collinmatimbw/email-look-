import re
import dns.resolver
from typing import Optional


def validate_email_format(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_domain_format(domain: str) -> bool:
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return bool(re.match(pattern, domain))


def extract_domain_from_email(email: str) -> Optional[str]:
    if validate_email_format(email):
        return email.split("@")[1].lower()
    return None


def is_business_domain(domain: str) -> bool:
    consumer_domains = {
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
        "aol.com", "icloud.com", "protonmail.com", "proton.me",
        "mail.com", "zoho.com", "yandex.com", "gmx.com",
        "fastmail.com", "tutanota.com", "live.com", "msn.com"
    }
    return domain.lower() not in consumer_domains


def sanitize_input(text: str) -> str:
    import html
    return html.escape(text.strip())


def check_mx_record(domain: str) -> list[dict]:
    try:
        answers = dns.resolver.resolve(domain, "MX")
        records = []
        for rdata in answers:
            records.append({
                "priority": rdata.preference,
                "host": str(rdata.exchange).rstrip(".")
            })
        return sorted(records, key=lambda x: x["priority"])
    except Exception:
        return []


def check_spf_record(domain: str) -> Optional[str]:
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        for rdata in answers:
            txt = "".join(part.decode() if isinstance(part, bytes) else part for part in rdata.strings)
            if txt.startswith("v=spf1"):
                return txt
    except Exception:
        pass
    return None


def check_dmarc_record(domain: str) -> Optional[str]:
    try:
        answers = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        for rdata in answers:
            txt = "".join(part.decode() if isinstance(part, bytes) else part for part in rdata.strings)
            if txt.startswith("v=DMARC1"):
                return txt
    except Exception:
        pass
    return None


def check_dkim_record(domain: str, selector: str = "default") -> Optional[str]:
    try:
        answers = dns.resolver.resolve(f"{selector}._domainkey.{domain}", "TXT")
        for rdata in answers:
            txt = "".join(part.decode() if isinstance(part, bytes) else part for part in rdata.strings)
            if txt.startswith("v=DKIM1"):
                return txt
    except Exception:
        pass
    return None
