"""Dependencies that identify the logged-in user."""

from http import HTTPStatus
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session
from app.auth.security import decode_access_token
from app.database import get_session
from app.users import repository as user_repository
from app.users.models import User

bearer_scheme = HTTPBearer(auto_error=False)

def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    if credentials is None:
        raise _unauthorized("Not authenticated")
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        raise _unauthorized("Invalid or expired token") from None

    user = user_repository.get_by_id(session, user_id)
    if user is None:
        raise _unauthorized("User no longer exists")
    if user.is_banned:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Account is banned"
        )
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]