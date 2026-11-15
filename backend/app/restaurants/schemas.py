"""Request and response schemas for restaurants."""

from pydantic import BaseModel, ConfigDict, Field


class RestaurantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    cuisine: str = Field(min_length=1, max_length=50)
    rating: float = Field(ge=0, le=5)


class RestaurantUpdate(RestaurantCreate):
    """PUT replaces all fields, so it has the same fields as create."""


class RestaurantRead(RestaurantCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int