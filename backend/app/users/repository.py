"""Database access for users."""

from sqlmodel import Session, select
from app.users.models import User

def get_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def get_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()




def save(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user