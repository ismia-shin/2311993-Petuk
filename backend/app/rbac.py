"""Role-based access control: the one place that says who can do what."""

from enum import Enum
from http import HTTPStatus
from fastapi import HTTPException
from app.auth.dependencies import CurrentUser
from app.users.models import Role, User

class Permission(str, Enum):
    CREATE_RESTAURANT = "create_restaurant"
    MANAGE_OWN_RESTAURANT = "manage_own_restaurant"
    MANAGE_ANY_RESTAURANT = "manage_any_restaurant"

ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.CUSTOMER: set(),
    Role.OWNER: {
        Permission.CREATE_RESTAURANT,
        Permission.MANAGE_OWN_RESTAURANT,
    },
    Role.ADMIN: {
        Permission.CREATE_RESTAURANT,
        Permission.MANAGE_ANY_RESTAURANT,
    },
}

def has_permission(user: User, permission: Permission) -> bool:
    try:
        role = Role(user.role)
    except ValueError:
        return False  
    return permission in ROLE_PERMISSIONS[role]

def can_manage(user: User, owner_id: int | None) -> bool:
    """True for an admin, or for an owner who owns the record."""
    if has_permission(user, Permission.MANAGE_ANY_RESTAURANT):
        return True
    return (
        has_permission(user, Permission.MANAGE_OWN_RESTAURANT)
        and owner_id is not None
        and owner_id == user.id
    )

def require_permission(permission: Permission):
    """Dependency: 401 if not logged in, 403 if the role lacks the permission."""

    def checker(current_user: CurrentUser) -> User:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="You do not have permission to do this",
            )
        return current_user

    return checker