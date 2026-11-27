"""Role-based access control"""

from enum import Enum
from http import HTTPStatus
from fastapi import HTTPException
from app.auth.dependencies import CurrentUser
from app.users.models import Role, User

class Permission(str, Enum):
    CREATE_RESTAURANT = "create_restaurant"
    MANAGE_OWN_RESTAURANT = "manage_own_restaurant"
    MANAGE_ANY_RESTAURANT = "manage_any_restaurant"
    WRITE_REVIEW = "write_review"
    DELETE_ANY_REVIEW = "delete_any_review"

ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.CUSTOMER: {Permission.WRITE_REVIEW},
    Role.OWNER: {
        Permission.CREATE_RESTAURANT,
        Permission.MANAGE_OWN_RESTAURANT,
    },
    Role.ADMIN: {
        Permission.CREATE_RESTAURANT,
        Permission.MANAGE_ANY_RESTAURANT,
        Permission.DELETE_ANY_REVIEW,
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

def ensure_can_manage(user: User, owner_id: int | None) -> None:
    """Raise 403 unless the user is an admin or owns the record."""
    if not can_manage(user, owner_id):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You do not have permission to manage this restaurant",
        )

def ensure_can_edit_review(user: User, author_id: int) -> None:
    """Only the author edits a review, not even an admin."""
    if user.id != author_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You can only edit your own review",
        )

def ensure_can_delete_review(user: User, author_id: int) -> None:
    """The author can delete a review, and so can an admin."""
    if user.id == author_id or has_permission(user, Permission.DELETE_ANY_REVIEW):
        return
    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail="You can only delete your own review",
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
