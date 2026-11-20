"""Request and response schemas for authentication."""

from typing import Literal
from pydantic import BaseModel, EmailStr, Field
from app.users.schemas import Name

class SignupRequest(BaseModel):
    email: EmailStr
    name: Name
    password: str = Field(min_length=8, max_length=128)
    # Admin can never be chosen here
    role: Literal["customer", "owner"] = "customer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"