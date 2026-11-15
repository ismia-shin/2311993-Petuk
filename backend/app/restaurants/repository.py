"""Database access for restaurants."""

from sqlmodel import Session, select

from app.restaurants.models import Restaurant


def get_all(session: Session) -> list[Restaurant]:
    statement = select(Restaurant).order_by(Restaurant.id)
    return list(session.exec(statement).all())


def get_by_id(session: Session, restaurant_id: int) -> Restaurant | None:
    return session.get(Restaurant, restaurant_id)


def save(session: Session, restaurant: Restaurant) -> Restaurant:
    """Insert a new restaurant or save changes to an existing one."""
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


def delete(session: Session, restaurant: Restaurant) -> None:
    session.delete(restaurant)
    session.commit()