import dns.resolver
import socket
from typing import Optional
from app.config import settings


async def get_dns_records(domain: str) -> dict:
    result = {
        "records": [],
        "mx_records": [],
        "spf": None,
        "dkim": None,
        "dmarc": None,
        "a_record": None,
        "aaaa_record": None,
        "ns_records": [],
        "cname_records": [],
        "txt_records": [],
    }

    try:
        a = dns.resolver.resolve(domain, "A", lifetime=settings.DNS_TIMEOUT)
        for rdata in a:
            ip = str(rdata)
            result["a_record"] = ip
            result["records"].append({"type": "A", "name": domain, "value": ip, "ttl": a.rrset.ttl if a.rrset else None})
    except Exception:
        pass

    try:
        aaaa = dns.resolver.resolve(domain, "AAAA", lifetime=settings.DNS_TIMEOUT)
        for rdata in aaaa:
            ip = str(rdata)
            result["aaaa_record"] = ip
            result["records"].append({"type": "AAAA", "name": domain, "value": ip, "ttl": aaaa.rrset.ttl if aaaa.rrset else None})
    except Exception:
        pass

    try:
        ns = dns.resolver.resolve(domain, "NS", lifetime=settings.DNS_TIMEOUT)
        for rdata in ns:
            ns_host = str(rdata).rstrip(".")
            result["ns_records"].append(ns_host)
            result["records"].append({"type": "NS", "name": domain, "value": ns_host, "ttl": ns.rrset.ttl if ns.rrset else None})
    except Exception:
        pass

    try:
        mx = dns.resolver.resolve(domain, "MX", lifetime=settings.DNS_TIMEOUT)
        for rdata in mx:
            record = {
                "priority": rdata.preference,
                "host": str(rdata.exchange).rstrip("."),
                "ttl": mx.rrset.ttl if mx.rrset else None
            }
            result["mx_records"].append(record)
            result["records"].append({"type": "MX", "name": domain, "value": f"{rdata.preference} {str(rdata.exchange).rstrip('.')}", "ttl": mx.rrset.ttl if mx.rrset else None})
    except Exception:
        pass

    try:
        txt = dns.resolver.resolve(domain, "TXT", lifetime=settings.DNS_TIMEOUT)
        for rdata in txt:
            txt_str = "".join(part.decode() if isinstance(part, bytes) else part for part in rdata.strings)
            result["txt_records"].append(txt_str)
            result["records"].append({"type": "TXT", "name": domain, "value": txt_str[:200], "ttl": txt.rrset.ttl if txt.rrset else None})
            if txt_str.startswith("v=spf1"):
                result["spf"] = txt_str
    except Exception:
        pass

    try:
        dmarc_txt = dns.resolver.resolve(f"_dmarc.{domain}", "TXT", lifetime=settings.DNS_TIMEOUT)
        for rdata in dmarc_txt:
            dmarc_str = "".join(part.decode() if isinstance(part, bytes) else part for part in rdata.strings)
            if dmarc_str.startswith("v=DMARC1"):
                result["dmarc"] = dmarc_str
    except Exception:
        pass

    selectors = ["default", "google", "selector1", "dkim", "mail"]
    for sel in selectors:
        try:
            dkim_txt = dns.resolver.resolve(f"{sel}._domainkey.{domain}", "TXT", lifetime=settings.DNS_TIMEOUT)
            for rdata in dkim_txt:
                dkim_str = "".join(part.decode() if isinstance(part, bytes) else part for part in rdata.strings)
                if dkim_str.startswith("v=DKIM1"):
                    result["dkim"] = dkim_str
                    break
            if result["dkim"]:
                break
        except Exception:
            continue

    try:
        cname = dns.resolver.resolve(domain, "CNAME", lifetime=settings.DNS_TIMEOUT)
        for rdata in cname:
            cname_target = str(rdata.target).rstrip(".")
            result["cname_records"].append(cname_target)
            result["records"].append({"type": "CNAME", "name": domain, "value": cname_target, "ttl": cname.rrset.ttl if cname.rrset else None})
    except Exception:
        pass

    return result


async def detect_hosting_provider(ip_address: Optional[str]) -> Optional[str]:
    if not ip_address:
        return None

    try:
        host = socket.gethostbyaddr(ip_address)
        hostname = host[0].lower()
    except Exception:
        return None

    providers = {
        "aws": ["amazonaws.com", "awsdns", "cloudfront.net"],
        "cloudflare": ["cloudflare.com"],
        "google": ["googleusercontent.com", "googledomains.com", "gcp", "1e100.net"],
        "microsoft": ["azure.com", "microsoft.com", "msn.com"],
        "digitalocean": ["digitalocean.com"],
        "linode": ["linode.com"],
        "ovh": ["ovh.com", "ovh.net"],
        "hetzner": ["hetzner.com", "hetzner.de"],
        "vultr": ["vultr.com"],
        "vercel": ["vercel.com"],
        "netlify": ["netlify.com"],
        "heroku": ["heroku.com", "herokudns.com"],
        "github": ["github.io", "githubpages.com"],
    }

    for provider, domains in providers.items():
        for d in domains:
            if d in hostname:
                return provider.capitalize()

    return "Unknown"
