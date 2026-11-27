"""Database model for menu items."""

from typing import Optional
from sqlmodel import Field, SQLModel

class MenuItem(SQLModel, table=True):
    __tablename__ = "menu_item"

    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True)
    name: str = Field(max_length=100)
    price: float  # in BDT (taka)
    description: Optional[str] = Field(default=None, max_length=255)