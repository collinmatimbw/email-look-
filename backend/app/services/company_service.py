from typing import Optional
import httpx
from bs4 import BeautifulSoup
import re
from app.services.ai_service import generate_company_summary


async def get_company_info(domain: str) -> dict:
    result = {
        "name": None,
        "domain": domain,
        "website": f"https://{domain}",
        "industry": None,
        "description": None,
        "employee_count": None,
        "founded_year": None,
        "headquarters": None,
        "social_media": {},
        "tech_stack": [],
        "ai_summary": None,
        "risk_level": "medium",
        "lead_score": 50
    }

    try:
        meta = await get_website_metadata(domain)
        result.update(meta)
    except Exception:
        pass

    try:
        tech = await detect_tech_stack(domain)
        result["tech_stack"] = tech
    except Exception:
        pass

    try:
        social = await find_social_media(domain)
        result["social_media"] = social
    except Exception:
        pass

    try:
        company_name = result["name"] or domain.split(".")[0].capitalize()
        summary_data = await generate_company_summary({
            "name": company_name,
            "domain": domain,
            "industry": result["industry"],
            "description": result["description"]
        })
        result["ai_summary"] = summary_data.get("summary")
    except Exception:
        pass

    return result


async def get_website_metadata(domain: str) -> dict:
    meta = {}
    url = f"https://{domain}"

    async with httpx.AsyncClient(timeout=10, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")

                og_title = soup.find("meta", property="og:title")
                if og_title:
                    meta["name"] = og_title.get("content")

                og_desc = soup.find("meta", property="og:description")
                if og_desc:
                    meta["description"] = og_desc.get("content")

                if not meta.get("name"):
                    title_tag = soup.find("title")
                    if title_tag:
                        meta["name"] = title_tag.string.strip() if title_tag.string else None

                if not meta.get("description"):
                    desc_tag = soup.find("meta", attrs={"name": "description"})
                    if desc_tag:
                        meta["description"] = desc_tag.get("content")

                for tag in soup.find_all("meta"):
                    prop = tag.get("property", "") or tag.get("name", "")
                    content = tag.get("content", "")
                    if "article:tag" in prop:
                        continue

                about_link = soup.find("a", href=re.compile(r"about", re.I))
                careers_link = soup.find("a", href=re.compile(r"career|jobs", re.I))
                if careers_link:
                    meta["employee_count"] = "Has careers page"

        except Exception:
            pass

    return meta


async def detect_tech_stack(domain: str) -> list[str]:
    tech = []
    url = f"https://{domain}"

    async with httpx.AsyncClient(timeout=10, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            html = resp.text.lower()
            headers = resp.headers

            if "x-powered-by" in headers:
                tech.append(headers["x-powered-by"])

            if "react" in html or "react.js" in html or "reactjs" in html:
                tech.append("React")
            if "next.js" in html or "nextjs" in html:
                tech.append("Next.js")
            if "vue" in html and "vuejs" not in html:
                tech.append("Vue.js")
            if "angular" in html:
                tech.append("Angular")
            if "jquery" in html:
                tech.append("jQuery")
            if "tailwind" in html or "tailwindcss" in html:
                tech.append("Tailwind CSS")
            if "bootstrap" in html:
                tech.append("Bootstrap")
            if "shopify" in html:
                tech.append("Shopify")
            if "wordpress" in html or "/wp-" in html:
                tech.append("WordPress")
            if "django" in html:
                tech.append("Django")
            if "laravel" in html:
                tech.append("Laravel")
            if "cloudflare" in html or "cloudflare" in str(headers).lower():
                tech.append("Cloudflare")
            if "google analytics" in html or "ga-" in html:
                tech.append("Google Analytics")
            if "gtm-" in html:
                tech.append("Google Tag Manager")
            if "facebook" in html and "pixel" in html:
                tech.append("Facebook Pixel")
            if "stripe" in html or "stripe.com" in html:
                tech.append("Stripe")

        except Exception:
            pass

    return list(set(tech))


async def find_social_media(domain: str) -> dict:
    social = {}
    url = f"https://{domain}"

    async with httpx.AsyncClient(timeout=10, follow_redirects=True, verify=False) as client:
        try:
            resp = await client.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            html = resp.text

            soup = BeautifulSoup(html, "lxml")

            for link in soup.find_all("a", href=True):
                href = link.get("href", "").lower()

                if "linkedin.com/company/" in href:
                    social["linkedin"] = link["href"]
                elif "twitter.com/" in href or "x.com/" in href:
                    social["twitter"] = link["href"]
                elif "facebook.com/" in href:
                    social["facebook"] = link["href"]
                elif "instagram.com/" in href:
                    social["instagram"] = link["href"]
                elif "youtube.com/" in href or "youtu.be/" in href:
                    social["youtube"] = link["href"]
                elif "github.com/" in href and "/company" not in href:
                    social["github"] = link["href"]
                elif "crunchbase.com/" in href:
                    social["crunchbase"] = link["href"]
                elif "angel.co/" in href or "angellist.com/" in href:
                    social["angellist"] = link["href"]

        except Exception:
            pass

    return social
