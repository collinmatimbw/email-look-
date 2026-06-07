import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_gravatar_hash(email: str) -> str:
    return hashlib.md5(email.lower().strip().encode()).hexdigest()


def get_gravatar_url(email: str, size: int = 200) -> str:
    h = generate_gravatar_hash(email)
    return f"https://www.gravatar.com/avatar/{h}?s={size}&d=mp"


def calculate_risk_score(domain_info: dict, company_info: dict) -> str:
    domain_info = domain_info or {}
    company_info = company_info or {}
    score = 0
    reasons = []

    if domain_info.get("spf_record"):
        score += 10
    else:
        reasons.append("No SPF record")

    if domain_info.get("dmarc_record"):
        score += 10
    else:
        reasons.append("No DMARC record")

    if domain_info.get("dkim_record"):
        score += 10
    else:
        reasons.append("No DKIM record")

    if domain_info.get("creation_date"):
        try:
            created = datetime.fromisoformat(domain_info["creation_date"].replace("Z", "+00:00"))
            age_days = (datetime.utcnow() - created).days
            if age_days > 365:
                score += 20
            elif age_days > 180:
                score += 10
            else:
                reasons.append("Domain is less than 6 months old")
        except Exception:
            pass

    if company_info.get("name"):
        score += 20
    if company_info.get("industry"):
        score += 10
    if company_info.get("social_media"):
        score += 10

    if score >= 70:
        return "low"
    elif score >= 40:
        return "medium"
    else:
        return "high"


def calculate_lead_score(company_info: dict) -> int:
    company_info = company_info or {}
    score = 0

    if company_info.get("name"):
        score += 15
    if company_info.get("website"):
        score += 15
    if company_info.get("industry"):
        score += 10
    if company_info.get("description"):
        score += 10
    if company_info.get("employee_count"):
        score += 10
    if company_info.get("founded_year"):
        score += 5
    if company_info.get("headquarters"):
        score += 5

    social_count = len(company_info.get("social_media", {}))
    score += min(social_count * 5, 15)

    tech_count = len(company_info.get("tech_stack", []))
    score += min(tech_count * 5, 15)

    return min(score, 100)


def format_timedelta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        return f"{total_seconds // 60}m"
    elif total_seconds < 86400:
        return f"{total_seconds // 3600}h"
    else:
        return f"{total_seconds // 86400}d"


def chunk_list(lst: list, size: int) -> list[list]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]
