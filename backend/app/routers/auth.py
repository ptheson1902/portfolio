"""Authentication router."""
from fastapi import APIRouter, Depends

from ..models.auth_schemas import TokenRequest, TokenResponse, AuthStatus, UserRole
from ..services.auth_service import auth_service
from ..middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(request: TokenRequest):
    """
    Verify admin token and return authentication status.
    This is a simple token verification - no session is created.
    The client should store the token and send it with each request.
    """
    return auth_service.verify_token(request.token)


@router.get("/verify", response_model=TokenResponse)
async def verify(user_role: UserRole = Depends(get_current_user)):
    """
    Verify the current token from Authorization header.
    Returns the user's role and authentication status.
    """
    return TokenResponse(
        valid=user_role == UserRole.OWNER,
        role=user_role,
        message="Token verified" if user_role == UserRole.OWNER else "Not authenticated as owner"
    )


@router.get("/status", response_model=AuthStatus)
async def get_status(user_role: UserRole = Depends(get_current_user)):
    """
    Get current authentication status.
    """
    return AuthStatus(
        authenticated=user_role == UserRole.OWNER,
        role=user_role
    )
