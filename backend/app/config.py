"""Application settings, read from environment variables."""

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or "sqlite:///./petuk.db"
    )
    jwt_secret: str = os.getenv(
        "JWT_SECRET", "dev-only-jwt-secret-change-me-0123456789abcdef"
    )
    password_pepper: str = os.getenv(
        "PASSWORD_PEPPER", "dev-only-pepper-change-me-0123456789abcdef"
    )
    access_token_minutes: int = 15
    refresh_token_days: int = 7
    cookie_secure: bool = bool(os.getenv("VERCEL"))

settings = Settings()

if os.getenv("VERCEL") and (
    "dev-only" in settings.jwt_secret or "dev-only" in settings.password_pepper
):
    raise RuntimeError("Set JWT_SECRET and PASSWORD_PEPPER on Vercel")