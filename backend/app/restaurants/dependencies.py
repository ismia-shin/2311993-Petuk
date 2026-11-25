"""Reusable permission dependencies for the restaurant routes."""

from typing import Annotated
from fastapi import Depends
from app.rbac import Permission, require_permission
from app.users.models import User

CanCreateRestaurant = Annotated[
    User, Depends(require_permission(Permission.CREATE_RESTAURANT))
]