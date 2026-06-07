import asyncio
import datetime
import hashlib
from typing import Optional
import httpx
from bs4 import BeautifulSoup
from app.utils.validators import extract_domain_from_email, is_business_domain, check_mx_record
from app.utils.helpers import get_gravatar_url
from app.services.dns_service import get_dns_records
from app.services.whois_service import get_whois_info
from app.services.company_service import get_company_info
from app.services.ai_service import generate_email_summary


def get_username_variations(username: str) -> list[str]:
    base = username.lower().strip()
    seen = {base}
    variants = [base]

    if "." in base:
        no_dot = base.replace(".", "")
        if no_dot not in seen:
            seen.add(no_dot)
            variants.append(no_dot)
        parts = base.split(".")
        if len(parts) >= 2:
            first = parts[0]
            if first not in seen:
                seen.add(first)
                variants.append(first)

    if "_" in base:
        no_underscore = base.replace("_", "")
        if no_underscore not in seen:
            seen.add(no_underscore)
            variants.append(no_underscore)

    if "-" in base:
        no_hyphen = base.replace("-", "")
        if no_hyphen not in seen:
            seen.add(no_hyphen)
            variants.append(no_hyphen)

    return variants


async def check_gravatar_profile(email: str) -> tuple[Optional[str], Optional[str], bool]:
    h = hashlib.md5(email.lower().strip().encode()).hexdigest()
    url = f"https://www.gravatar.com/{h}.json"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url, headers={"User-Agent": "EmailInsight/1.0"})
            if r.status_code == 200:
                d = r.json()
                entries = d.get("entry", [{}])
                if entries:
                    display = entries[0].get("displayName") or entries[0].get("preferredUsername")
                    avatar = entries[0].get("thumbnailUrl") or f"https://www.gravatar.com/avatar/{h}?s=200"
                    return avatar, display, True
    except Exception:
        pass
    return get_gravatar_url(email), None, False


def extract_possible_name(profiles: list[dict], gravatar_name: Optional[str]) -> Optional[str]:
    if gravatar_name:
        return gravatar_name
    for p in profiles:
        name = p.get("display_name")
        if name and len(name) > 2 and " " not in name.strip():
            continue
        if name and len(name) > 2:
            return name
        bio = p.get("bio", "")
        if bio and len(bio) > 5:
            import re
            match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", bio)
            if match:
                return match.group(1)
    return None


async def lookup_email(email: str) -> dict:
    domain = extract_domain_from_email(email)
    if not domain:
        return {"error": "Invalid email format", "status": "error"}

    username = email.split("@")[0].lower()
    username_variants = get_username_variations(username)

    gravatar_url, gravatar_name, gravatar_has = await check_gravatar_profile(email)

    result = {
        "email": email,
        "domain": domain,
        "username": username,
        "is_business": is_business_domain(domain),
        "possible_name": None,
        "known_usernames": username_variants,
        "gravatar_url": gravatar_url,
        "gravatar_has_profile": gravatar_has,
        "public_profiles": [],
        "profile_count": 0,
        "mx_records": [],
        "dns_records": [],
        "whois": {},
        "company": None,
        "ai_summary": None,
        "risk_score": "medium",
    }

    public_profiles = await find_public_profiles(username, username_variants)
    result["public_profiles"] = public_profiles
    result["profile_count"] = len(public_profiles)
    result["possible_name"] = extract_possible_name(public_profiles, gravatar_name)

    mx = check_mx_record(domain)
    result["mx_records"] = mx

    if result["is_business"]:
        dns = await get_dns_records(domain)
        result["dns_records"] = dns.get("records", [])
        whois = await get_whois_info(domain)
        result["whois"] = whois
        company = await get_company_info(domain)
        result["company"] = company

    summaries = await generate_email_summary(result)
    result["ai_summary"] = summaries.get("summary")
    result["risk_score"] = summaries.get("risk_score", "medium")

    return result


async def find_public_profiles(username: str, username_variants: list[str]) -> list[dict]:
    found = []

    async with httpx.AsyncClient(timeout=10, headers={
        "User-Agent": "EmailInsight/1.0 (OSINT Research Tool)",
        "Accept": "application/json",
    }) as client:

        targets = [username] + [v for v in username_variants if v != username]

        for uname in targets:
            if len(found) >= 12:
                break

            # GitHub API
            try:
                r = await client.get(f"https://api.github.com/users/{uname}")
                if r.status_code == 200:
                    d = r.json()
                    found.append({
                        "name": "GitHub",
                        "url": d.get("html_url", f"https://github.com/{uname}"),
                        "type": "Development",
                        "category": "dev",
                        "avatar": d.get("avatar_url"),
                        "display_name": d.get("name"),
                        "bio": d.get("bio"),
                        "location": d.get("location"),
                        "details": {
                            "Public Repos": str(d.get("public_repos", 0)),
                            "Followers": str(d.get("followers", 0)),
                            "Account Created": (d.get("created_at") or "").split("T")[0] if d.get("created_at") else "",
                        }
                    })
                    continue
            except Exception:
                pass

            # Reddit API
            try:
                r = await client.get(
                    f"https://www.reddit.com/user/{uname}/about.json",
                    headers={"User-Agent": "EmailInsight/1.0"}
                )
                if r.status_code == 200:
                    d = r.json().get("data", {})
                    created = d.get("created_utc", 0)
                    cd = datetime.datetime.utcfromtimestamp(created).strftime("%Y-%m-%d") if created else ""
                    found.append({
                        "name": "Reddit",
                        "url": f"https://reddit.com/user/{uname}",
                        "type": "Community",
                        "category": "dev",
                        "avatar": (d.get("icon_img") or "").split("?")[0],
                        "display_name": d.get("subreddit", {}).get("title") if d.get("subreddit") else "",
                        "bio": d.get("subreddit", {}).get("public_description", "") if d.get("subreddit") else "",
                        "location": "",
                        "details": {
                            "Karma": str(d.get("total_karma", 0)),
                            "Created": cd,
                        }
                    })
                    continue
            except Exception:
                pass

            # Dev.to API
            try:
                r = await client.get(f"https://dev.to/api/users/by_username?url={uname}")
                if r.status_code == 200:
                    d = r.json()
                    found.append({
                        "name": "Dev.to",
                        "url": f"https://dev.to/{uname}",
                        "type": "Writing",
                        "category": "dev",
                        "avatar": d.get("profile_image"),
                        "display_name": d.get("name"),
                        "bio": d.get("summary"),
                        "location": d.get("location"),
                        "details": {
                            "Posts": str(d.get("articles_count", 0)),
                            "Joined": d.get("joined_at", ""),
                        }
                    })
                    continue
            except Exception:
                pass

            # Hacker News API
            try:
                r = await client.get(f"https://hacker-news.firebaseio.com/v0/user/{uname}.json")
                if r.status_code == 200 and r.json() and r.json().get("id"):
                    d = r.json()
                    created = d.get("created", 0)
                    cd = datetime.datetime.utcfromtimestamp(created).strftime("%Y-%m-%d") if created else ""
                    found.append({
                        "name": "Hacker News",
                        "url": f"https://news.ycombinator.com/user?id={uname}",
                        "type": "Community",
                        "category": "dev",
                        "avatar": "",
                        "display_name": d.get("id"),
                        "bio": "",
                        "location": "",
                        "details": {
                            "Karma": str(d.get("karma", 0)),
                            "Created": cd,
                        }
                    })
                    continue
            except Exception:
                pass

            # GitLab API
            try:
                r = await client.get(f"https://gitlab.com/api/v4/users?username={uname}")
                if r.status_code == 200 and len(r.json()) > 0:
                    d = r.json()[0]
                    found.append({
                        "name": "GitLab",
                        "url": d.get("web_url", f"https://gitlab.com/{uname}"),
                        "type": "Development",
                        "category": "dev",
                        "avatar": d.get("avatar_url"),
                        "display_name": d.get("name"),
                        "bio": d.get("bio"),
                        "location": "",
                        "details": {
                            "Public Projects": str(d.get("public_projects", 0)),
                            "Followers": str(d.get("followers", 0)),
                        }
                    })
                    continue
            except Exception:
                pass

            # Keybase API
            try:
                r = await client.get(f"https://keybase.io/_/api/1.0/user/lookup.json?username={uname}")
                if r.status_code == 200:
                    d = r.json()
                    if d.get("status", {}).get("code") == 0:
                        them = d.get("them", [{}])[0]
                        found.append({
                            "name": "Keybase",
                            "url": f"https://keybase.io/{uname}",
                            "type": "Security",
                            "category": "security",
                            "avatar": them.get("pictures", {}).get("primary", {}).get("url", ""),
                            "display_name": them.get("profile", {}).get("full_name", ""),
                            "bio": them.get("profile", {}).get("bio", ""),
                            "location": them.get("profile", {}).get("location", ""),
                            "details": {
                                "Devices": str(len(them.get("devices", []))),
                                "Proofs": str(len(them.get("proofs_summary", {}).get("all", []))),
                            }
                        })
                        continue
            except Exception:
                pass

            # Docker Hub API
            try:
                r = await client.get(f"https://hub.docker.com/v2/users/{uname}")
                if r.status_code == 200:
                    d = r.json()
                    found.append({
                        "name": "Docker Hub",
                        "url": f"https://hub.docker.com/u/{uname}",
                        "type": "Registry",
                        "category": "registry",
                        "avatar": "",
                        "display_name": d.get("full_name", ""),
                        "bio": "",
                        "location": d.get("location", ""),
                        "details": {
                            "Repos": str(d.get("repo_count", 0)),
                            "Stars": str(d.get("star_count", 0)),
                        }
                    })
                    continue
            except Exception:
                pass

            # npm API
            try:
                r = await client.get(f"https://registry.npmjs.org/-/v1/search?text=maintainer:{uname}&size=1")
                if r.status_code == 200:
                    total = r.json().get("total", 0)
                    if total > 0:
                        found.append({
                            "name": "npm",
                            "url": f"https://npmjs.com/~{uname}",
                            "type": "Registry",
                            "category": "registry",
                            "avatar": "",
                            "display_name": uname,
                            "bio": "",
                            "location": "",
                            "details": {"Packages": str(total)}
                        })
                        continue
            except Exception:
                pass

            # Bitbucket API
            try:
                r = await client.get(f"https://api.bitbucket.org/2.0/users/{uname}")
                if r.status_code == 200:
                    d = r.json()
                    found.append({
                        "name": "Bitbucket",
                        "url": f"https://bitbucket.org/{uname}",
                        "type": "Development",
                        "category": "dev",
                        "avatar": d.get("links", {}).get("avatar", {}).get("href", ""),
                        "display_name": d.get("display_name", ""),
                        "bio": "",
                        "location": d.get("location", ""),
                        "details": {
                            "Created": (d.get("created_on") or "").split("T")[0] if d.get("created_on") else "",
                        }
                    })
                    continue
            except Exception:
                pass

            # Crates.io API
            try:
                r = await client.get(f"https://crates.io/api/v1/users/{uname}", headers={"Accept": "application/json"})
                if r.status_code == 200:
                    u = r.json().get("user", {})
                    found.append({
                        "name": "Crates.io",
                        "url": f"https://crates.io/users/{uname}",
                        "type": "Registry",
                        "category": "registry",
                        "avatar": "",
                        "display_name": u.get("name", ""),
                        "bio": "",
                        "location": "",
                        "details": {"Crates": str(u.get("crate_count", 0))}
                    })
                    continue
            except Exception:
                pass

            # PyPI (scrape)
            try:
                r = await client.get(f"https://pypi.org/user/{uname}/")
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, "html.parser")
                    pkg_count = len(soup.select(".package-snippet"))
                    if pkg_count > 0:
                        name_tag = soup.select_one("h1 span")
                        found.append({
                            "name": "PyPI",
                            "url": f"https://pypi.org/user/{uname}/",
                            "type": "Registry",
                            "category": "registry",
                            "avatar": "",
                            "display_name": name_tag.get_text(strip=True) if name_tag else uname,
                            "bio": "",
                            "location": "",
                            "details": {"Packages": str(pkg_count)}
                        })
                        continue
            except Exception:
                pass

    return found
