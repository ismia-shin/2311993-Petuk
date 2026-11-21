"""Database access for refresh tokens."""

from sqlmodel import Session, col, select
from app.auth.models import RefreshToken
from app.utils import utc_now

def save(session: Session, token: RefreshToken) -> RefreshToken:
    session.add(token)
    session.commit()
    session.refresh(token)
    return token


def get_by_hash(session: Session, token_hash: str) -> RefreshToken | None:
    statement = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    return session.exec(statement).first()


def revoke(session: Session, token: RefreshToken) -> None:
    token.revoked_at = utc_now()
    save(session, token)

def revoke_all_for_user(session: Session, user_id: int) -> None:
    statement = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        col(RefreshToken.revoked_at).is_(None),
    )
    for token in session.exec(statement).all():
        token.revoked_at = utc_now()
        session.add(token)
    session.commit()