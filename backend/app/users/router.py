"""REST endpoints for the logged-in user's own profile."""

from http import HTTPStatus
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session
from app.auth.dependencies import CurrentUser
from app.database import get_session
from app.users import service
from app.users.schemas import PasswordChange, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def get_me(current_user: CurrentUser):
    """Return the logged-in user."""
    return current_user

@router.put("/me", response_model=UserRead)
def update_me(
    data: UserUpdate,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    return service.update_profile(session, current_user, data)

@router.put("/me/password", status_code=HTTPStatus.NO_CONTENT)
def change_my_password(
    data: PasswordChange,
    current_user: CurrentUser,
    session: Session = Depends(get_session),
):
    service.change_password(session, current_user, data)
    return Response(status_code=HTTPStatus.NO_CONTENT)