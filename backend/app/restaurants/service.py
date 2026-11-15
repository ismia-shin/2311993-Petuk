"""Business logic for restaurants."""

from http import HTTPStatus

from fastapi import HTTPException
from sqlmodel import Session

from app.restaurants import repository
from app.restaurants.models import Restaurant
from app.restaurants.schemas import RestaurantCreate, RestaurantUpdate


def list_restaurants(session: Session) -> list[Restaurant]:
    return repository.get_all(session)


def get_restaurant(session: Session, restaurant_id: int) -> Restaurant:
    restaurant = repository.get_by_id(session, restaurant_id)
    if restaurant is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Restaurant not found"
        )
    return restaurant


def create_restaurant(session: Session, data: RestaurantCreate) -> Restaurant:
    restaurant = Restaurant(**data.model_dump())
    return repository.save(session, restaurant)


def update_restaurant(
    session: Session, restaurant_id: int, data: RestaurantUpdate
) -> Restaurant:
    restaurant = get_restaurant(session, restaurant_id)
    for field, value in data.model_dump().items():
        setattr(restaurant, field, value)
    return repository.save(session, restaurant)


def delete_restaurant(session: Session, restaurant_id: int) -> None:
    restaurant = get_restaurant(session, restaurant_id)
    repository.delete(session, restaurant)