"""Database model for the activity (audit) log."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel
from app.utils import utc_now

class AuditAction(str, Enum):
    LOGIN = "login"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_CHANGED = "password_changed"
    ROLE_CHANGED = "role_changed"
    USER_BANNED = "user_banned"
    USER_UNBANNED = "user_unbanned"

class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="app_user.id", index=True)
    email: Optional[str] = Field(default=None, max_length=255)
    action: str = Field(max_length=50, index=True)
    detail: Optional[str] = Field(default=None, max_length=255)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False, index=True),
    )