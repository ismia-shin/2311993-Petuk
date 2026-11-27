"""Business logic for restaurants."""

from http import HTTPStatus
from fastapi import HTTPException
from sqlmodel import Session
from app.rbac import ensure_can_manage
from app.restaurants import repository
from app.restaurants.models import Restaurant
from app.restaurants.schemas import (
    RestaurantCreate,
    RestaurantRead,
    RestaurantUpdate,
)
from app.reviews import repository as review_repository
from app.reviews.schemas import RatingSummary
from app.users.models import User

def _with_ratings(
    restaurant: Restaurant, summary: RatingSummary | None
) -> RestaurantRead:
    result = RestaurantRead.model_validate(restaurant)
    if summary is not None:
        result.ratings = summary
    return result

def list_restaurants(session: Session) -> list[RestaurantRead]:
    restaurants = repository.get_all(session)
    summaries = review_repository.get_rating_summaries(session)
    return [_with_ratings(r, summaries.get(r.id)) for r in restaurants]

def get_restaurant(session: Session, restaurant_id: int) -> Restaurant:
    restaurant = repository.get_by_id(session, restaurant_id)
    if restaurant is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Restaurant not found"
        )
    return restaurant

def get_restaurant_read(session: Session, restaurant_id: int) -> RestaurantRead:
    restaurant = get_restaurant(session, restaurant_id)
    summaries = review_repository.get_rating_summaries(session, restaurant.id)
    return _with_ratings(restaurant, summaries.get(restaurant.id))

def create_restaurant(
    session: Session, data: RestaurantCreate, creator: User
) -> Restaurant:
    restaurant = Restaurant(**data.model_dump(), owner_id=creator.id)
    return repository.save(session, restaurant)

def update_restaurant(
    session: Session, restaurant_id: int, data: RestaurantUpdate, user: User
) -> RestaurantRead:
    restaurant = get_restaurant(session, restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    for field, value in data.model_dump().items():
        setattr(restaurant, field, value)
    repository.save(session, restaurant)
    return get_restaurant_read(session, restaurant_id)

def delete_restaurant(session: Session, restaurant_id: int, user: User) -> None:
    restaurant = get_restaurant(session, restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    repository.delete(session, restaurant)