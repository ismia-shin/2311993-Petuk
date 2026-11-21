"""Database model for users."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel
from app.utils import utc_now

class Role(str, Enum):
    CUSTOMER = "customer"
    OWNER = "owner"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "app_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    role: str = Field(default=Role.CUSTOMER.value, max_length=20)
    is_banned: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )