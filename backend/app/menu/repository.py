"""Database access for menu items."""

from sqlmodel import Session, select
from app.menu.models import MenuItem

def get_by_restaurant(session: Session, restaurant_id: int) -> list[MenuItem]:
    statement = (
        select(MenuItem)
        .where(MenuItem.restaurant_id == restaurant_id)
        .order_by(MenuItem.id)
    )
    return list(session.exec(statement).all())

def get_by_id(session: Session, item_id: int) -> MenuItem | None:
    return session.get(MenuItem, item_id)

def save(session: Session, item: MenuItem) -> MenuItem:
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def delete(session: Session, item: MenuItem) -> None:
    session.delete(item)
    session.commit()