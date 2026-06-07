import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy import String as SaString
from sqlalchemy.orm import relationship
from app.database import Base


class Search(Base):
    __tablename__ = "searches"

    id = Column(SaString(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(SaString(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), index=True)
    search_type = Column(String(50), default="email")
    result_data = Column(JSON, default=dict)
    status = Column(String(20), default="completed")
    risk_score = Column(String(20))
    ai_summary = Column(Text)
    is_saved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="searches")
    company = relationship("Company", back_populates="search", uselist=False, cascade="all, delete-orphan")
    domain_info = relationship("Domain", back_populates="search", uselist=False, cascade="all, delete-orphan")
