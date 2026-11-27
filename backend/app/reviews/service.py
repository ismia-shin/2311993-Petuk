"""Business logic for reviews."""

from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.rbac import ensure_can_delete_review, ensure_can_edit_review
from app.restaurants import service as restaurant_service
from app.reviews import repository
from app.reviews.models import Review
from app.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate
from app.users.models import User

ALREADY_REVIEWED = "You have already reviewed this restaurant"

def _to_read(review: Review, user_name: str) -> ReviewRead:
    return ReviewRead(**review.model_dump(), user_name=user_name)

def _get_review(session: Session, review_id: int) -> Review:
    review = repository.get_by_id(session, review_id)
    if review is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Review not found"
        )
    return review

def list_reviews(
    session: Session, restaurant_id: int, offset: int, limit: int
) -> list[ReviewRead]:
    # Gives 404 if the restaurant does not exist
    restaurant_service.get_restaurant(session, restaurant_id)
    rows = repository.get_by_restaurant(session, restaurant_id, offset, limit)
    return [_to_read(review, name) for review, name in rows]

def create_review(
    session: Session, restaurant_id: int, data: ReviewCreate, user: User
) -> ReviewRead:
    restaurant = restaurant_service.get_restaurant(session, restaurant_id)
    if repository.get_by_user_and_restaurant(session, user.id, restaurant.id):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=ALREADY_REVIEWED)
    review = Review(
        **data.model_dump(), restaurant_id=restaurant.id, user_id=user.id
    )
    try:
        saved = repository.save(session, review)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail=ALREADY_REVIEWED
        ) from None
    return _to_read(saved, user.name)

def update_review(
    session: Session, review_id: int, data: ReviewUpdate, user: User
) -> ReviewRead:
    review = _get_review(session, review_id)
    ensure_can_edit_review(user, review.user_id)
    for field, value in data.model_dump().items():
        setattr(review, field, value)
    return _to_read(repository.save(session, review), user.name)

def delete_review(session: Session, review_id: int, user: User) -> None:
    review = _get_review(session, review_id)
    ensure_can_delete_review(user, review.user_id)
    repository.delete(session, review)