"""Reusable permission dependencies for the review routes."""

from typing import Annotated
from fastapi import Depends
from app.rbac import Permission, require_permission
from app.users.models import User

CanWriteReview = Annotated[
    User, Depends(require_permission(Permission.WRITE_REVIEW))
]