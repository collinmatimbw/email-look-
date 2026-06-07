import httpx
from typing import Optional
from app.utils.helpers import generate_gravatar_hash


async def check_gravatar(email: str) -> Optional[str]:
    h = generate_gravatar_hash(email)
    url = f"https://www.gravatar.com/avatar/{h}?d=404&s=200"

    async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
        try:
            resp = await client.head(url)
            if resp.status_code == 200:
                return f"https://www.gravatar.com/avatar/{h}?s=200&d=mp"
        except Exception:
            pass

    return None
