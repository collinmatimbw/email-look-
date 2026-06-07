from pydantic import BaseModel
from typing import Optional


class CompanyResponse(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    employee_count: Optional[str] = None
    founded_year: Optional[str] = None
    headquarters: Optional[str] = None
    social_media: dict = {}
    tech_stack: list[str] = []
    ai_summary: Optional[str] = None
    risk_level: Optional[str] = None
    lead_score: Optional[int] = None


class AiSummaryRequest(BaseModel):
    text: str
    summary_type: str = "company"
