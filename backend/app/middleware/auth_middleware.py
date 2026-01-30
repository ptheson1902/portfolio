"""Authentication middleware for FastAPI."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from ..models.auth_schemas import UserRole
from ..services.auth_service import auth_service

# Optional bearer token - doesn't fail if not provided
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> UserRole:
    """
    Get the current user's role from the Authorization header.
    Returns VISITOR if no token provided.
    Returns OWNER if valid admin token provided.
    """
    if not credentials:
        return UserRole.VISITOR

    token = credentials.credentials
    return auth_service.get_role_from_token(token)


def require_owner(user_role: UserRole = Depends(get_current_user)) -> UserRole:
    """
    Dependency that requires OWNER role.
    Raises 403 Forbidden if user is not OWNER.
    """
    if user_role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner privileges required. Please provide a valid admin token."
        )
    return user_role


def get_optional_owner(user_role: UserRole = Depends(get_current_user)) -> bool:
    """
    Returns True if user is OWNER, False otherwise.
    Does not raise exception.
    """
    return user_role == UserRole.OWNER
