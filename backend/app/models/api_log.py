import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy import String as SaString
from app.database import Base


class ApiLog(Base):
    __tablename__ = "api_logs"

    id = Column(SaString(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(SaString(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer)
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    response_time_ms = Column(Integer)
    request_body = Column(Text)
    response_body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
