from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.domain import DomainResponse, DNSRecord, MXRecord
from app.services.dns_service import get_dns_records, detect_hosting_provider
from app.services.whois_service import get_whois_info
from app.utils.validators import validate_domain_format
from app.middleware.auth_middleware import get_optional_user
from app.models.user import User

router = APIRouter(prefix="/api/domain", tags=["Domain Intelligence"])


@router.get("/lookup", response_model=DomainResponse)
async def domain_lookup(
    domain: str = Query(..., description="Domain name to lookup"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    domain = domain.strip().lower()

    if not validate_domain_format(domain):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid domain format"
        )

    dns_data = await get_dns_records(domain)
    whois_data = await get_whois_info(domain)
    hosting = await detect_hosting_provider(dns_data.get("a_record"))

    mx_records = []
    for mx in dns_data.get("mx_records", []):
        mx_records.append(MXRecord(priority=mx["priority"], host=mx["host"]))

    dns_records = []
    for rec in dns_data.get("records", []):
        dns_records.append(DNSRecord(
            type=rec["type"],
            name=rec["name"],
            value=rec.get("value", ""),
            ttl=rec.get("ttl")
        ))

    return DomainResponse(
        domain_name=domain,
        registrar=whois_data.get("registrar"),
        creation_date=whois_data.get("creation_date"),
        expiration_date=whois_data.get("expiration_date"),
        name_servers=whois_data.get("name_servers", []),
        mx_records=mx_records,
        spf_record=dns_data.get("spf"),
        dkim_record=dns_data.get("dkim"),
        dmarc_record=dns_data.get("dmarc"),
        hosting_provider=hosting,
        ip_address=dns_data.get("a_record"),
        dnssec_enabled=whois_data.get("dnssec", False),
        dns_records=dns_records
    )


@router.get("/dns")
async def domain_dns(
    domain: str = Query(..., description="Domain name"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not validate_domain_format(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    records = await get_dns_records(domain)
    return records


@router.get("/whois")
async def domain_whois(
    domain: str = Query(..., description="Domain name"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not validate_domain_format(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    info = await get_whois_info(domain)
    return info


@router.get("/security")
async def domain_security(
    domain: str = Query(..., description="Domain name"),
    current_user: Optional[User] = Depends(get_optional_user)
):
    if not validate_domain_format(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format")

    dns = await get_dns_records(domain)
    return {
        "domain": domain,
        "spf": dns.get("spf"),
        "dkim": dns.get("dkim"),
        "dmarc": dns.get("dmarc"),
        "has_spf": dns.get("spf") is not None,
        "has_dkim": dns.get("dkim") is not None,
        "has_dmarc": dns.get("dmarc") is not None,
        "security_score": sum([
            33 if dns.get("spf") else 0,
            33 if dns.get("dkim") else 0,
            34 if dns.get("dmarc") else 0
        ])
    }
