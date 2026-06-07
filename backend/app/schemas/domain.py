from pydantic import BaseModel
from typing import Optional


class DomainLookupRequest(BaseModel):
    domain: str


class DNSRecord(BaseModel):
    type: str
    name: str
    value: str
    ttl: Optional[int] = None


class MXRecord(BaseModel):
    priority: int
    host: str


class DomainResponse(BaseModel):
    domain_name: str
    registrar: Optional[str] = None
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    name_servers: list[str] = []
    mx_records: list[MXRecord] = []
    spf_record: Optional[str] = None
    dkim_record: Optional[str] = None
    dmarc_record: Optional[str] = None
    hosting_provider: Optional[str] = None
    ip_address: Optional[str] = None
    dnssec_enabled: bool = False
    dns_records: list[DNSRecord] = []
