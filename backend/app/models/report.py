import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy import String as SaString
from sqlalchemy.orm import relationship
from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(SaString(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(SaString(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    search_ids = Column(JSON, default=list)
    report_type = Column(String(50), default="email_summary")
    format_type = Column(String(10), default="pdf")
    title = Column(String(255))
    data = Column(JSON, default=dict)
    file_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")
