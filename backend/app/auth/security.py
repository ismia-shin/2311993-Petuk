"""Password hashing and token helpers."""

import hashlib
import hmac
import secrets
from datetime import timedelta
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from app.config import settings
from app.utils import utc_now

JWT_ALGORITHM = "HS256"

_hasher = PasswordHasher()

def _apply_pepper(password: str) -> str:
    """Mix the secret pepper into the password before hashing."""
    return hmac.new(
        settings.password_pepper.encode(), password.encode(), hashlib.sha256
    ).hexdigest()

def hash_password(password: str) -> str:
    return _hasher.hash(_apply_pepper(password))

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _hasher.verify(password_hash, _apply_pepper(password))
    except (VerificationError, InvalidHashError):
        return False

def create_access_token(user_id: int, role: str) -> str:
    now = utc_now()
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Return the token payload, or raise jwt.PyJWTError if it is bad."""
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[JWT_ALGORITHM],
        options={"require": ["exp", "sub"]},
    )
    if payload.get("type") != "access":
        raise jwt.InvalidTokenError("Not an access token")
    return payload

def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()

def generate_refresh_token() -> tuple[str, str]:
    """Return (raw token for the cookie, hash for the database)."""
    raw_token = secrets.token_urlsafe(48)
    return raw_token, hash_token(raw_token)