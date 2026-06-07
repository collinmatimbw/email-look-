from typing import Optional
from app.config import settings


async def generate_email_summary(data: dict) -> dict:
    if not settings.OPENAI_API_KEY:
        return {
            "summary": generate_fallback_email_summary(data),
            "risk_score": data.get("risk_score", "medium")
        }

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        domain = data.get("domain", "unknown")
        is_business = data.get("is_business", False)
        mx_count = len(data.get("mx_records", []))
        has_spf = bool(data.get("dns_records") and any(r.get("type") == "TXT" and "v=spf1" in r.get("value", "") for r in data["dns_records"]))
        has_dmarc = bool(data.get("dns_records") and any(r.get("type") == "TXT" and "v=DMARC1" in r.get("value", "") for r in data["dns_records"]))

        prompt = f"""Analyze this email domain for OSINT/business intelligence:

Domain: {domain}
Business Domain: {is_business}
MX Records Found: {mx_count}
SPF Configured: {has_spf}
DMARC Configured: {has_dmarc}
Company: {data.get('company')}

Provide a brief analysis including:
1. What this domain is likely used for
2. Security posture assessment
3. Risk level (low/medium/high)
4. Key business insights

Keep it concise (2-3 paragraphs)."""

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an OSINT and business intelligence analyst. Analyze domains and provide concise, factual insights based on available data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )

        text = response.choices[0].message.content

        if "high" in text.lower():
            risk = "high"
        elif "medium" in text.lower():
            risk = "medium"
        else:
            risk = "low"

        return {"summary": text, "risk_score": risk}

    except Exception:
        return {
            "summary": generate_fallback_email_summary(data),
            "risk_score": data.get("risk_score", "medium")
        }


async def generate_company_summary(data: dict) -> dict:
    if not settings.OPENAI_API_KEY:
        return {"summary": generate_fallback_company_summary(data)}

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = f"""Generate a professional business summary for:

Company: {data.get('name')}
Domain: {data.get('domain')}
Industry: {data.get('industry', 'Unknown')}
Description: {data.get('description', 'No description available')}

Provide a brief company overview including likely business focus, potential size, and industry relevance."""

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a business intelligence analyst. Generate professional company summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.3
        )

        return {"summary": response.choices[0].message.content}

    except Exception:
        return {"summary": generate_fallback_company_summary(data)}


def generate_fallback_email_summary(data: dict) -> str:
    email = data.get("email", "Unknown")
    domain = data.get("domain", "Unknown")
    possible_name = data.get("possible_name")
    profiles = data.get("public_profiles", [])
    profile_count = data.get("profile_count", 0)
    is_business = data.get("is_business", False)

    lines = [f"Intelligence report for {email}."]

    if possible_name:
        lines.append(f"Possible identity: {possible_name}.")

    if profile_count > 0:
        names = [p["name"] for p in profiles[:5]]
        lines.append(f"Found {profile_count} public profile(s) including {', '.join(names)}.")
    else:
        lines.append("No public profiles found for this email address.")

    if is_business:
        mx_count = len(data.get("mx_records", []))
        lines.append(f"Business domain with {mx_count} mail server(s).")
        if data.get("company"):
            company_name = data["company"].get("name", domain.split(".")[0].title())
            lines.append(f"Associated with {company_name}.")
    else:
        lines.append(f"Consumer email provider ({domain}).")

    return " ".join(lines)


def generate_fallback_company_summary(data: dict) -> str:
    name = data.get("name", data.get("domain", "Unknown"))
    industry = data.get("industry", "various industries")
    return f"{name} operates in {industry}. The company uses the domain {data.get('domain', 'unknown')} for its online presence."
