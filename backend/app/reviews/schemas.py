"""Request and response schemas for reviews."""

from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
Rating = Annotated[int, Field(ge=1, le=5)]

class ReviewCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    taste: Rating
    atmosphere: Rating
    cleanliness: Rating
    price: Rating
    service: Rating
    comment: str | None = Field(default=None, max_length=500)

class ReviewUpdate(ReviewCreate):
    """PUT replaces all fields, so it has the same fields as create."""

class ReviewRead(ReviewCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: int
    user_id: int
    user_name: str
    created_at: datetime

class RatingSummary(BaseModel):
    """Average scores of one restaurant. All averages are empty without reviews."""

    count: int = 0
    overall: float | None = None
    taste: float | None = None
    atmosphere: float | None = None
    cleanliness: float | None = None
    price: float | None = None
    service: float | None = None