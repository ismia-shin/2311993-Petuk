"""REST endpoints for restaurants."""

from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from app.database import get_session
from app.restaurants import service
from app.restaurants.schemas import (
    RestaurantCreate,
    RestaurantRead,
    RestaurantUpdate,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[RestaurantRead])
def list_restaurants(session: Session = Depends(get_session)):
    """Read List: return all restaurants."""
    return service.list_restaurants(session)


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    """Read Single: return one restaurant by id."""
    return service.get_restaurant(session, restaurant_id)


@router.post("", response_model=RestaurantRead, status_code=HTTPStatus.CREATED)
def create_restaurant(
    data: RestaurantCreate, session: Session = Depends(get_session)
):
    """Create: add a new restaurant."""
    return service.create_restaurant(session, data)


@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    session: Session = Depends(get_session),
):
    """Update: replace the fields of an existing restaurant."""
    return service.update_restaurant(session, restaurant_id, data)


@router.delete("/{restaurant_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    """Delete: remove a restaurant."""
    service.delete_restaurant(session, restaurant_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)