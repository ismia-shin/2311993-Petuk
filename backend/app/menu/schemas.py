"""Request and response schemas for menu items."""

from pydantic import BaseModel, ConfigDict, Field

class MenuItemCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0, le=1_000_000)
    description: str | None = Field(default=None, max_length=255)

class MenuItemUpdate(MenuItemCreate):
    """PUT replaces all fields, so it has the same fields as create."""

class MenuItemRead(MenuItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: int