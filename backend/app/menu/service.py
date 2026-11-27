"""Business logic for menu items."""

from http import HTTPStatus

from fastapi import HTTPException
from sqlmodel import Session
from app.menu import repository
from app.menu.models import MenuItem
from app.menu.schemas import MenuItemCreate, MenuItemUpdate
from app.rbac import ensure_can_manage
from app.restaurants import service as restaurant_service
from app.users.models import User

def _get_item(session: Session, item_id: int) -> MenuItem:
    item = repository.get_by_id(session, item_id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Menu item not found"
        )
    return item

def list_menu_items(session: Session, restaurant_id: int) -> list[MenuItem]:
    # Gives 404 if the restaurant does not exist
    restaurant_service.get_restaurant(session, restaurant_id)
    return repository.get_by_restaurant(session, restaurant_id)

def create_menu_item(
    session: Session, restaurant_id: int, data: MenuItemCreate, user: User
) -> MenuItem:
    restaurant = restaurant_service.get_restaurant(session, restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    item = MenuItem(**data.model_dump(), restaurant_id=restaurant.id)
    return repository.save(session, item)

def update_menu_item(
    session: Session, item_id: int, data: MenuItemUpdate, user: User
) -> MenuItem:
    item = _get_item(session, item_id)
    restaurant = restaurant_service.get_restaurant(session, item.restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    for field, value in data.model_dump().items():
        setattr(item, field, value)
    return repository.save(session, item)

def delete_menu_item(session: Session, item_id: int, user: User) -> None:
    item = _get_item(session, item_id)
    restaurant = restaurant_service.get_restaurant(session, item.restaurant_id)
    ensure_can_manage(user, restaurant.owner_id)
    repository.delete(session, item)