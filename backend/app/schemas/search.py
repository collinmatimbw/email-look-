from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime


class EmailLookupRequest(BaseModel):
    email: EmailStr


class EmailLookupResponse(BaseModel):
    id: str
    email: str
    domain: str
    search_type: str
    status: str
    result_data: dict
    risk_score: Optional[str] = None
    ai_summary: Optional[str] = None
    company: Optional[dict] = None
    domain_info: Optional[dict] = None
    created_at: datetime


class SearchHistoryItem(BaseModel):
    id: str
    email: str
    domain: Optional[str] = None
    search_type: str
    status: str
    risk_score: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SearchAnalytics(BaseModel):
    total_searches: int
    unique_domains: int
    unique_emails: int
    searches_today: int
    searches_this_week: int
    searches_this_month: int
    top_domains: list[dict]
    recent_searches: list[SearchHistoryItem]
    searches_by_day: list[dict]


class ExportRequest(BaseModel):
    search_ids: list[str]
    format_type: str = "pdf"
