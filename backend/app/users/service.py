"""Business logic for users."""

from http import HTTPStatus
from fastapi import HTTPException
from sqlmodel import Session
from app.auth import repository as auth_repository
from app.auth.security import hash_password, verify_password
from app.users import repository as user_repository
from app.users.models import User
from app.users.schemas import PasswordChange, UserUpdate

def update_profile(session: Session, user: User, data: UserUpdate) -> User:
    user.name = data.name
    return user_repository.save(session, user)

def change_password(session: Session, user: User, data: PasswordChange) -> None:
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Current password is incorrect",
        )
    user.password_hash = hash_password(data.new_password)
    user_repository.save(session, user)

    auth_repository.revoke_all_for_user(session, user.id)