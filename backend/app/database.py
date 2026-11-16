"""Database engine and session handling."""

from sqlalchemy.pool import NullPool
from sqlmodel import Session, create_engine

from app.config import settings

DATABASE_URL = settings.database_url

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
        
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
        
    DATABASE_URL = DATABASE_URL.replace("&supa=base-pooler.x", "").replace(
        "?supa=base-pooler.x", ""
    )
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        connect_args={"prepare_threshold": None},
    )

def get_session():
    """FastAPI dependency: one database session per request."""
    with Session(engine) as session:
        yield session