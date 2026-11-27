"""Business logic for restaurants."""

from http import HTTPStatus

from fastapi import HTTPException
from sqlmodel import Session

from app.rbac import ensure_can_manage
from app.restaurants import repository
from app.restaurants.models import Restaurant
from app.restaurants.schemas import RestaurantCreate, RestaurantUpdate
from app.users.models import User


def list_restaurants(session: Session) -> list[Restaurant]:
    return repository.get_all(session)


def get_restaurant(session: Session, restaurant_id: int) -> Restaurant:
    restaurant = repository.get_by_id(session, restaurant_id)
    if restaurant is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Restaurant not found"
        )
    return restaurant


def create_restaurant(session: Session, data: RestaurantCreate, creator: User) -> Restaurant:
    restaurant = Restaurant(**data.model_dump(), owner_id=creator.id)
    return repository.save(session, restaurant)


def update_restaurant(session: Session, restaurant_id: int, data: RestaurantUpdate, user: User) -> Restaurant:
    restaurant = get_restaurant(session, restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    for field, value in data.model_dump().items():
        setattr(restaurant, field, value)
    return repository.save(session, restaurant)


def delete_restaurant(session: Session, restaurant_id: int, user: User) -> None:
    restaurant = get_restaurant(session, restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    repository.delete(session, restaurant)