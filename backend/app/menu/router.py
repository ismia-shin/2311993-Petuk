"""REST endpoints for menu items."""

from http import HTTPStatus
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session
from app.auth.dependencies import CurrentUser
from app.database import get_session
from app.menu import service
from app.menu.schemas import MenuItemCreate, MenuItemRead, MenuItemUpdate

router = APIRouter(tags=["menu"])

@router.get(
    "/restaurants/{restaurant_id}/menu-items", response_model=list[MenuItemRead]
)
def list_menu_items(restaurant_id: int, session: Session = Depends(get_session)):
    """Read List: public."""
    return service.list_menu_items(session, restaurant_id)

@router.post(
    "/restaurants/{restaurant_id}/menu-items",
    response_model=MenuItemRead,
    status_code=HTTPStatus.CREATED,
)
def create_menu_item(
    restaurant_id: int,
    data: MenuItemCreate,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Create: the restaurant's owner or an admin."""
    return service.create_menu_item(session, restaurant_id, data, current_user)

@router.put("/menu-items/{item_id}", response_model=MenuItemRead)
def update_menu_item(
    item_id: int,
    data: MenuItemUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Update: the restaurant's owner or an admin."""
    return service.update_menu_item(session, item_id, data, current_user)

@router.delete("/menu-items/{item_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_menu_item(
    item_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Delete: the restaurant's owner or an admin."""
    service.delete_menu_item(session, item_id, current_user)
    return Response(status_code=HTTPStatus.NO_CONTENT)