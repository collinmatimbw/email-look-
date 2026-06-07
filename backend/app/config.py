from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Email Insight API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str
    DATABASE_URL_ASYNC: Optional[str] = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    GRAVATAR_ENABLED: bool = True
    DNS_TIMEOUT: int = 5
    WHOIS_TIMEOUT: int = 10

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 30
    RATE_LIMIT_PERIOD: int = 60

    REDIS_URL: Optional[str] = None

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "https://email-insight.vercel.app"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
