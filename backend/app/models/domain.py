import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy import String as SaString
from sqlalchemy.orm import relationship
from app.database import Base


class Domain(Base):
    __tablename__ = "domains"

    id = Column(SaString(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    search_id = Column(SaString(36), ForeignKey("searches.id", ondelete="CASCADE"), nullable=False)
    domain_name = Column(String(255), nullable=False, index=True)
    registrar = Column(String(255))
    creation_date = Column(String(50))
    expiration_date = Column(String(50))
    updated_date = Column(String(50))
    name_servers = Column(JSON, default=list)
    mx_records = Column(JSON, default=list)
    spf_record = Column(String(500))
    dkim_record = Column(String(500))
    dmarc_record = Column(String(500))
    hosting_provider = Column(String(255))
    ip_address = Column(String(50))
    registrar_abuse_contact = Column(String(255))
    dnssec_enabled = Column(Boolean, default=False)
    raw_whois = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    search = relationship("Search", back_populates="domain_info")
