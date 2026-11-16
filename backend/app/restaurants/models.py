"""Database model for restaurants."""

from typing import Optional
from sqlmodel import Field, SQLModel

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    area: str = Field(max_length=100)
    cuisine: str = Field(max_length=50)
    address: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)