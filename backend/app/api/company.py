from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.company import CompanyResponse, AiSummaryRequest
from app.services.company_service import get_company_info, get_website_metadata, detect_tech_stack, find_social_media
from app.services.ai_service import generate_company_summary
from app.utils.validators import validate_domain_format
from app.middleware.auth_middleware import get_optional_user
from app.models.user import User

router = APIRouter(prefix="/api/company", tags=["Company Intelligence"])


@router.get("/lookup", response_model=CompanyResponse)
async def company_lookup(
    domain: str = Query(..., description="Company domain"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    domain = domain.strip().lower()

    if not validate_domain_format(domain):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid domain format"
        )

    info = await get_company_info(domain)

    return CompanyResponse(
        name=info.get("name"),
        domain=domain,
        website=info.get("website"),
        industry=info.get("industry"),
        description=info.get("description"),
        employee_count=info.get("employee_count"),
        founded_year=info.get("founded_year"),
        headquarters=info.get("headquarters"),
        social_media=info.get("social_media", {}),
        tech_stack=info.get("tech_stack", []),
        ai_summary=info.get("ai_summary"),
        risk_level=info.get("risk_level", "medium"),
        lead_score=info.get("lead_score", 50)
    )


@router.get("/metadata")
async def company_metadata(
    domain: str = Query(..., description="Company domain"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not validate_domain_format(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    meta = await get_website_metadata(domain)
    return meta


@router.get("/tech-stack")
async def company_tech_stack(
    domain: str = Query(..., description="Company domain"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not validate_domain_format(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    tech = await detect_tech_stack(domain)
    return {"domain": domain, "technologies": tech}


@router.get("/social")
async def company_social(
    domain: str = Query(..., description="Company domain"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not validate_domain_format(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    social = await find_social_media(domain)
    return {"domain": domain, "social_media": social}


@router.post("/ai-summary")
async def ai_company_summary(
    request: AiSummaryRequest,
    current_user: Optional[User] = Depends(get_optional_user)
):
    data = {"name": request.text, "description": request.text}
    result = await generate_company_summary(data)
    return result
