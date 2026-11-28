"""REST endpoints for reviews."""

from http import HTTPStatus
from fastapi import APIRouter, Depends, Query, Response
from sqlmodel import Session
from app.auth.dependencies import CurrentUser
from app.database import get_session
from app.reviews import service
from app.reviews.dependencies import CanWriteReview
from app.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(tags=["reviews"])

@router.get("/restaurants/{restaurant_id}/reviews", response_model=list[ReviewRead])
def list_reviews(
    restaurant_id: int,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=50),
    session: Session = Depends(get_session),
):
    """Read List: public, newest first."""
    return service.list_reviews(session, restaurant_id, offset, limit)

@router.post(
    "/restaurants/{restaurant_id}/reviews",
    response_model=ReviewRead,
    status_code=HTTPStatus.CREATED,
)
def create_review(
    restaurant_id: int,
    data: ReviewCreate,
    current_user: CanWriteReview,
    session: Session = Depends(get_session),
):
    """Create: customers only, one review per restaurant."""
    return service.create_review(session, restaurant_id, data, current_user)

@router.put("/reviews/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Update: the author only."""
    return service.update_review(session, review_id, data, current_user)

@router.delete("/reviews/{review_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    """Delete: the author, or an admin."""
    service.delete_review(session, review_id, current_user)
    return Response(status_code=HTTPStatus.NO_CONTENT)