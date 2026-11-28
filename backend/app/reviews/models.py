"""Database model for reviews."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, UniqueConstraint
from sqlmodel import Field, SQLModel
from app.utils import utc_now

class Review(SQLModel, table=True):
    __tablename__ = "review"
    __table_args__ = (
        UniqueConstraint("restaurant_id", "user_id", name="uq_review_restaurant_user"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True)
    user_id: int = Field(foreign_key="app_user.id", index=True)
    taste: int
    atmosphere: int
    cleanliness: int
    price: int  
    service: int
    comment: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )