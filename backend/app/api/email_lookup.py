from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.search import EmailLookupRequest, EmailLookupResponse, SearchHistoryItem
from app.services.email_service import lookup_email
from app.services.gravatar_service import check_gravatar
from app.utils.validators import validate_email_format, extract_domain_from_email
from app.utils.helpers import calculate_risk_score, calculate_lead_score
from app.middleware.auth_middleware import get_current_user, get_optional_user
from app.models.user import User
from app.models.search import Search
from app.models.company import Company
from app.models.domain import Domain
from datetime import datetime

router = APIRouter(prefix="/api/email", tags=["Email Lookup"])


@router.post("/lookup", response_model=EmailLookupResponse)
async def lookup_email_endpoint(
    request: EmailLookupRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    email = request.email.strip().lower()

    if not validate_email_format(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    domain = extract_domain_from_email(email)

    result = await lookup_email(email)

    risk_score = calculate_risk_score(
        {"spf_record": result.get("dns_records"), "dmarc_record": result.get("whois"), "creation_date": (result.get("whois") or {}).get("creation_date")},
        result.get("company") or {}
    )

    gravatar = await check_gravatar(email)
    if gravatar:
        result["gravatar_url"] = gravatar

    search_record = None
    if current_user:
        search_record = Search(
            user_id=current_user.id,
            email=email,
            domain=domain,
            search_type="email",
            result_data=result,
            status="completed",
            risk_score=risk_score,
            ai_summary=result.get("ai_summary"),
            created_at=datetime.utcnow()
        )
        db.add(search_record)
        db.flush()

        company_data = result.get("company")
        if company_data:
            company_record = Company(
                search_id=search_record.id,
                name=company_data.get("name"),
                domain=domain,
                website=company_data.get("website"),
                industry=company_data.get("industry"),
                description=company_data.get("description"),
                employee_count=company_data.get("employee_count"),
                founded_year=company_data.get("founded_year"),
                headquarters=company_data.get("headquarters"),
                social_media=company_data.get("social_media"),
                tech_stack=company_data.get("tech_stack"),
                ai_summary=company_data.get("ai_summary"),
                risk_level=risk_score,
                lead_score=calculate_lead_score(company_data),
            )
            db.add(company_record)

        domain_data = result.get("whois", {})
        domain_record = Domain(
            search_id=search_record.id,
            domain_name=domain,
            registrar=domain_data.get("registrar"),
            creation_date=domain_data.get("creation_date"),
            expiration_date=domain_data.get("expiration_date"),
            updated_date=domain_data.get("updated_date"),
            name_servers=domain_data.get("name_servers", []),
            mx_records=result.get("mx_records", []),
            spf_record=result.get("dns_records")[0].get("value") if result.get("dns_records") else None,
            hosting_provider=result.get("hosting_provider"),
            dnssec_enabled=domain_data.get("dnssec", False),
            raw_whois=domain_data.get("raw"),
        )
        db.add(domain_record)
        db.commit()
        db.refresh(search_record)

    return EmailLookupResponse(
        id=str(search_record.id) if search_record else "",
        email=email,
        domain=domain,
        search_type="email",
        status="completed",
        result_data=result,
        risk_score=risk_score,
        ai_summary=result.get("ai_summary"),
        company=result.get("company"),
        domain_info=result.get("whois"),
        created_at=search_record.created_at if search_record else datetime.utcnow()
    )


@router.get("/gravatar")
async def get_gravatar(email: str = Query(..., description="Email address")):
    if not validate_email_format(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    url = await check_gravatar(email)
    return {"url": url, "has_gravatar": url is not None}
