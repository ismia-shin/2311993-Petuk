"""Database access for reviews."""

from sqlmodel import Session, col, func, select
from app.reviews.models import Review
from app.reviews.schemas import RatingSummary
from app.users.models import User

def get_by_restaurant(
    session: Session, restaurant_id: int, offset: int, limit: int
) -> list[tuple[Review, str]]:
    """Newest first, together with the name of each reviewer."""
    statement = (
        select(Review, User.name)
        .join(User, col(User.id) == Review.user_id)
        .where(Review.restaurant_id == restaurant_id)
        .order_by(col(Review.created_at).desc(), col(Review.id).desc())
        .offset(offset)
        .limit(limit)
    )
    return [(review, name) for review, name in session.exec(statement).all()]

def get_by_id(session: Session, review_id: int) -> Review | None:
    return session.get(Review, review_id)


def get_by_user_and_restaurant(
    session: Session, user_id: int, restaurant_id: int
) -> Review | None:
    statement = select(Review).where(
        Review.user_id == user_id, Review.restaurant_id == restaurant_id
    )
    return session.exec(statement).first()

def save(session: Session, review: Review) -> Review:
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

def delete(session: Session, review: Review) -> None:
    session.delete(review)
    session.commit()

def get_rating_summaries(
    session: Session, restaurant_id: int | None = None
) -> dict[int, RatingSummary]:
    """Average of each category per restaurant. Restaurants without reviews are missing."""
    statement = select(
        Review.restaurant_id,
        func.count(Review.id),
        func.avg(Review.taste),
        func.avg(Review.atmosphere),
        func.avg(Review.cleanliness),
        func.avg(Review.price),
        func.avg(Review.service),
    ).group_by(Review.restaurant_id)
    if restaurant_id is not None:
        statement = statement.where(Review.restaurant_id == restaurant_id)

    summaries: dict[int, RatingSummary] = {}
    for row in session.exec(statement).all():
        rid, count, *averages = row
        taste, atmosphere, cleanliness, price, service = (float(a) for a in averages)
        summaries[rid] = RatingSummary(
            count=count,
            overall=round((taste + atmosphere + cleanliness + price + service) / 5, 1),
            taste=round(taste, 1),
            atmosphere=round(atmosphere, 1),
            cleanliness=round(cleanliness, 1),
            price=round(price, 1),
            service=round(service, 1),
        )
    return summaries