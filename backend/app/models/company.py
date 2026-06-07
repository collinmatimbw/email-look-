import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, JSON
from sqlalchemy import String as SaString
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(SaString(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    search_id = Column(SaString(36), ForeignKey("searches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), index=True)
    domain = Column(String(255), index=True)
    website = Column(String(500))
    industry = Column(String(255))
    description = Column(Text)
    employee_count = Column(String(50))
    founded_year = Column(String(10))
    headquarters = Column(String(255))
    social_media = Column(JSON, default=dict)
    tech_stack = Column(JSON, default=list)
    ai_summary = Column(Text)
    risk_level = Column(String(20))
    lead_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    search = relationship("Search", back_populates="company")
