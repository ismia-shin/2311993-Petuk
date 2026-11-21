"""REST endpoints for authentication."""

from http import HTTPStatus
from fastapi import APIRouter, Cookie, Depends, Response
from sqlmodel import Session
from app.auth import service
from app.auth.dependencies import CurrentUser
from app.auth.schemas import LoginRequest, SignupRequest, TokenResponse
from app.config import settings
from app.database import get_session
from app.users.schemas import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE = "refresh_token"
COOKIE_PATH = "/api/v1/auth"

def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=token,
        max_age=settings.refresh_token_days * 24 * 60 * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path=COOKIE_PATH,
    )

def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        path=COOKIE_PATH,
    )

@router.post("/signup", response_model=UserRead, status_code=HTTPStatus.CREATED)
def signup(data: SignupRequest, session: Session = Depends(get_session)):
    """Create a customer or owner account."""
    return service.signup(session, data)

@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    """Check the password, return an access token and set the refresh cookie."""
    access_token, refresh_token = service.login(session, data)
    _set_refresh_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token)

@router.post("/refresh", response_model=TokenResponse)
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    session: Session = Depends(get_session),
):
    """Use the refresh cookie to get a new access token (and a new cookie)."""
    access_token, new_refresh_token = service.refresh(session, refresh_token)
    _set_refresh_cookie(response, new_refresh_token)
    return TokenResponse(access_token=access_token)

@router.post("/logout", status_code=HTTPStatus.NO_CONTENT)
def logout(
    refresh_token: str | None = Cookie(default=None),
    session: Session = Depends(get_session),
):
    """End this session."""
    service.logout(session, refresh_token)
    response = Response(status_code=HTTPStatus.NO_CONTENT)
    _clear_refresh_cookie(response)
    return response

@router.post("/logout-all", status_code=HTTPStatus.NO_CONTENT)
def logout_all(current_user: CurrentUser, session: Session = Depends(get_session)):
    """End every session of the logged-in user."""
    service.logout_all(session, current_user)
    response = Response(status_code=HTTPStatus.NO_CONTENT)
    _clear_refresh_cookie(response)
    return response