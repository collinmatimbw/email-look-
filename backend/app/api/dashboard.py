from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta
from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.models.search import Search
from app.models.company import Company

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = today_start.replace(day=1)

    base = db.query(Search).filter(Search.user_id == current_user.id)
    total = base.count()
    today = base.filter(Search.created_at >= today_start).count()
    this_month = base.filter(Search.created_at >= month_start).count()

    unique_domains = base.filter(Search.domain.isnot(None)).distinct(Search.domain).count()
    unique_emails = base.distinct(Search.email).count()

    recent = (
        base.order_by(Search.created_at.desc())
        .limit(5)
        .all()
    )

    top_domains = (
        db.query(Search.domain, func.count(Search.id).label("count"))
        .filter(Search.user_id == current_user.id, Search.domain.isnot(None))
        .group_by(Search.domain)
        .order_by(func.count(Search.id).desc())
        .limit(5)
        .all()
    )

    searches_by_day = (
        db.query(
            cast(Search.created_at, Date).label("date"),
            func.count(Search.id).label("count")
        )
        .filter(
            Search.user_id == current_user.id,
            Search.created_at >= (today_start - timedelta(days=30))
        )
        .group_by(cast(Search.created_at, Date))
        .order_by(cast(Search.created_at, Date))
        .all()
    )

    companies = db.query(Company).join(Search).filter(Search.user_id == current_user.id).all()
    avg_lead = sum(c.lead_score or 0 for c in companies) / len(companies) if companies else 0

    risk_distribution = {
        "low": base.filter(Search.risk_score == "low").count(),
        "medium": base.filter(Search.risk_score == "medium").count(),
        "high": base.filter(Search.risk_score == "high").count(),
    }

    return {
        "total_searches": total,
        "searches_today": today,
        "searches_this_month": this_month,
        "unique_domains": unique_domains,
        "unique_emails": unique_emails,
        "avg_lead_score": round(avg_lead, 1),
        "risk_distribution": risk_distribution,
        "recent_searches": [
            {
                "id": str(s.id),
                "email": s.email,
                "domain": s.domain,
                "risk_score": s.risk_score,
                "created_at": s.created_at.isoformat() if s.created_at else None
            }
            for s in recent
        ],
        "top_domains": [
            {"domain": d[0], "count": d[1]}
            for d in top_domains
        ],
        "searches_by_day": [
            {"date": str(d[0]), "count": d[1]}
            for d in searches_by_day
        ]
    }
