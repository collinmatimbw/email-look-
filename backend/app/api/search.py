from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from typing import Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.search import SearchHistoryItem, SearchAnalytics, ExportRequest
from app.services.export_service import export_to_json, export_to_csv, export_to_html
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.models.search import Search
from app.models.company import Company

router = APIRouter(prefix="/api/search", tags=["Search History"])


@router.get("/history", response_model=list[SearchHistoryItem])
async def get_search_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Search).filter(Search.user_id == current_user.id)

    if search_type:
        query = query.filter(Search.search_type == search_type)

    query = query.order_by(Search.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)
    searches = query.all()

    return [
        SearchHistoryItem(
            id=str(s.id),
            email=s.email,
            domain=s.domain,
            search_type=s.search_type,
            status=s.status,
            risk_score=s.risk_score,
            created_at=s.created_at
        )
        for s in searches
    ]


@router.get("/analytics", response_model=SearchAnalytics)
async def get_search_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())
    month_start = today_start.replace(day=1)

    base = db.query(Search).filter(Search.user_id == current_user.id)

    total_searches = base.count()
    searches_today = base.filter(Search.created_at >= today_start).count()
    searches_this_week = base.filter(Search.created_at >= week_start).count()
    searches_this_month = base.filter(Search.created_at >= month_start).count()

    unique_domains = base.filter(Search.domain.isnot(None)).distinct(Search.domain).count()
    unique_emails = base.distinct(Search.email).count()

    top_domains = (
        db.query(Search.domain, func.count(Search.id).label("count"))
        .filter(Search.user_id == current_user.id, Search.domain.isnot(None))
        .group_by(Search.domain)
        .order_by(func.count(Search.id).desc())
        .limit(10)
        .all()
    )

    recent = (
        base.order_by(Search.created_at.desc())
        .limit(10)
        .all()
    )

    searches_by_day = (
        db.query(
            cast(Search.created_at, Date).label("date"),
            func.count(Search.id).label("count")
        )
        .filter(
            Search.user_id == current_user.id,
            Search.created_at >= month_start
        )
        .group_by(cast(Search.created_at, Date))
        .order_by(cast(Search.created_at, Date))
        .all()
    )

    companies = db.query(Company).join(Search).filter(Search.user_id == current_user.id).all()
    total_lead_score = sum(c.lead_score or 0 for c in companies)
    avg_lead_score = total_lead_score / len(companies) if companies else 0

    return SearchAnalytics(
        total_searches=total_searches,
        unique_domains=unique_domains,
        unique_emails=unique_emails,
        searches_today=searches_today,
        searches_this_week=searches_this_week,
        searches_this_month=searches_this_month,
        top_domains=[{"domain": d[0], "count": d[1]} for d in top_domains],
        recent_searches=[
            SearchHistoryItem(
                id=str(s.id),
                email=s.email,
                domain=s.domain,
                search_type=s.search_type,
                status=s.status,
                risk_score=s.risk_score,
                created_at=s.created_at
            )
            for s in recent
        ],
        searches_by_day=[{"date": str(d[0]), "count": d[1]} for d in searches_by_day]
    )


@router.get("/{search_id}")
async def get_search_detail(
    search_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    search = db.query(Search).filter(
        Search.id == search_id,
        Search.user_id == current_user.id
    ).first()

    if not search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search not found"
        )

    return {
        "id": str(search.id),
        "email": search.email,
        "domain": search.domain,
        "search_type": search.search_type,
        "status": search.status,
        "result_data": search.result_data,
        "risk_score": search.risk_score,
        "ai_summary": search.ai_summary,
        "created_at": search.created_at,
        "company": db.query(Company).filter(Company.search_id == search.id).first(),
        "domain_info": search.domain_info
    }


@router.delete("/{search_id}")
async def delete_search(
    search_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    search = db.query(Search).filter(
        Search.id == search_id,
        Search.user_id == current_user.id
    ).first()

    if not search:
        raise HTTPException(status_code=404, detail="Search not found")

    db.delete(search)
    db.commit()
    return {"message": "Search deleted successfully"}


@router.post("/export")
async def export_search_data(
    request: ExportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    searches = (
        db.query(Search)
        .filter(
            Search.id.in_(request.search_ids),
            Search.user_id == current_user.id
        )
        .all()
    )

    if not searches:
        raise HTTPException(status_code=404, detail="No searches found")

    data = []
    for s in searches:
        item = {
            "email": s.email,
            "domain": s.domain,
            "type": s.search_type,
            "risk_score": s.risk_score,
            "ai_summary": s.ai_summary,
            "searched_at": s.created_at.isoformat() if s.created_at else None
        }
        if s.result_data:
            item.update(s.result_data)
        data.append(item)

    if request.format_type == "json":
        content = export_to_json(data)
        media_type = "application/json"
        filename = "email-insight-export.json"
    elif request.format_type == "csv":
        content = export_to_csv(data)
        media_type = "text/csv"
        filename = "email-insight-export.csv"
    else:
        combined = {
            "export_date": datetime.utcnow().isoformat(),
            "total_searches": len(data),
            "searches": data
        }
        content = export_to_html(combined)
        media_type = "text/html"
        filename = "email-insight-report.html"

    from fastapi.responses import Response
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
