"""Request and response schemas for restaurants."""

from pydantic import BaseModel, ConfigDict, Field

class RestaurantCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    area: str = Field(min_length=1, max_length=100)
    cuisine: str = Field(min_length=1, max_length=50)
    address: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=500)


class RestaurantUpdate(RestaurantCreate):
    """PUT replaces all fields, so it has the same fields as create."""


class RestaurantRead(RestaurantCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int

