"""REST endpoints for restaurants."""

from http import HTTPStatus
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session
from app.auth.dependencies import CurrentUser
from app.database import get_session
from app.restaurants import service
from app.restaurants.dependencies import CanCreateRestaurant
from app.restaurants.schemas import (
    RestaurantCreate,
    RestaurantRead,
    RestaurantUpdate,
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[RestaurantRead])
def list_restaurants(session: Session = Depends(get_session)):
    """Read List: public."""
    return service.list_restaurants(session)


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    """Read Single: public."""
    return service.get_restaurant_read(session, restaurant_id)


@router.post("", response_model=RestaurantRead, status_code=HTTPStatus.CREATED)
def create_restaurant(
    data: RestaurantCreate,
    current_user: CanCreateRestaurant,
    session: Session = Depends(get_session),
):
    """Create: owners and admins only. The creator becomes the owner."""
    return service.create_restaurant(session, data, current_user)


@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Update: the restaurant's owner or an admin."""
    return service.update_restaurant(session, restaurant_id, data, current_user)


@router.delete("/{restaurant_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Delete: the restaurant's owner or an admin."""
    service.delete_restaurant(session, restaurant_id, current_user)
    return Response(status_code=HTTPStatus.NO_CONTENT)
