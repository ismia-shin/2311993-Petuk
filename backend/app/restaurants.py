import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.pool import NullPool
from sqlmodel import Field, Session, SQLModel, create_engine, select


DATABASE_URL = (
    os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite:///./petuk.db"
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
    DATABASE_URL = DATABASE_URL.replace("&supa=base-pooler.x", "").replace(
        "?supa=base-pooler.x", ""
    )
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        connect_args={"prepare_threshold": None},
    )


def init_db() -> None:
    """Create the restaurant table if it does not exist yet."""
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class RestaurantBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    cuisine: str = Field(min_length=1, max_length=50)
    rating: float = Field(ge=0, le=5)

class Restaurant(RestaurantBase, table=True):
    """The database table."""

    id: Optional[int] = Field(default=None, primary_key=True)


class RestaurantCreate(RestaurantBase):
    """What the client sends when creating or updating."""


class RestaurantRead(RestaurantBase):
    """What the API sends back."""

    id: int


router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("", response_model=list[RestaurantRead])
def list_restaurants(session: Session = Depends(get_session)):
    """Read List: return all restaurants."""
    return session.exec(select(Restaurant).order_by(Restaurant.id)).all()


@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    """Read Single: return one restaurant by id."""
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.post(
    "", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED
)
def create_restaurant(
    data: RestaurantCreate, session: Session = Depends(get_session)
):
    """Create: add a new restaurant."""
    restaurant = Restaurant.model_validate(data)
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantCreate,
    session: Session = Depends(get_session),
):
    """Update: replace name, cuisine and rating of an existing restaurant."""
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurant.name = data.name
    restaurant.cuisine = data.cuisine
    restaurant.rating = data.rating
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    """Delete: remove a restaurant."""
    restaurant = session.get(Restaurant, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    session.delete(restaurant)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)