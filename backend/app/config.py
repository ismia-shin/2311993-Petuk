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


settings = Settings()