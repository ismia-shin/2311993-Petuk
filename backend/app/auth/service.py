"""Business logic for authentication."""

from datetime import timedelta
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.auth import repository as auth_repository
from app.auth.models import RefreshToken
from app.auth.schemas import LoginRequest, SignupRequest
from app.auth.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.config import settings
from app.users import repository as user_repository
from app.users.models import User
from app.utils import as_utc, utc_now

def signup(session: Session, data: SignupRequest) -> User:
    email = data.email.lower()
    if user_repository.get_by_email(session, email) is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email already registered"
        )
    user = User(
        email=email,
        name=data.name,
        password_hash=hash_password(data.password),
        role=data.role,
    )
    try:
        return user_repository.save(session, user)
    except IntegrityError:
        # Two signups with the same email at the same moment
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email already registered"
        ) from None

def _issue_tokens(session: Session, user: User) -> tuple[str, str]:
    """Create an access token and a new stored refresh token."""
    raw_token, token_hash = generate_refresh_token()
    expires_at = utc_now() + timedelta(days=settings.refresh_token_days)
    auth_repository.save(
        session,
        RefreshToken(user_id=user.id, token_hash=token_hash, expires_at=expires_at),
    )
    return create_access_token(user.id, user.role), raw_token

def login(session: Session, data: LoginRequest) -> tuple[str, str]:
    """Return (access token, raw refresh token)."""
    user = user_repository.get_by_email(session, data.email.lower())
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid email or password"
        )
    if user.is_banned:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Account is banned"
        )
    return _issue_tokens(session, user)

def refresh(session: Session, raw_token: str | None) -> tuple[str, str]:
    """Swap a valid refresh token for a new pair (rotation)."""
    invalid = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid refresh token"
    )
    if not raw_token:
        raise invalid
    stored = auth_repository.get_by_hash(session, hash_token(raw_token))
    if (
        stored is None
        or stored.revoked_at is not None
        or as_utc(stored.expires_at) <= utc_now()
    ):
        raise invalid
    user = user_repository.get_by_id(session, stored.user_id)
    if user is None or user.is_banned:
        raise invalid
    # Rotation: the old token can never be used again
    auth_repository.revoke(session, stored)
    return _issue_tokens(session, user)

def logout(session: Session, raw_token: str | None) -> None:
    if not raw_token:
        return
    stored = auth_repository.get_by_hash(session, hash_token(raw_token))
    if stored is not None and stored.revoked_at is None:
        auth_repository.revoke(session, stored)

def logout_all(session: Session, user: User) -> None:
    auth_repository.revoke_all_for_user(session, user.id)