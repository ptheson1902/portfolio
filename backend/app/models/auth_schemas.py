"""Authentication related Pydantic schemas."""
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class UserRole(str, Enum):
    """User roles for RBAC."""
    OWNER = "owner"
    VISITOR = "visitor"


class TokenRequest(BaseModel):
    """Request to verify/login with admin token."""
    token: str


class TokenResponse(BaseModel):
    """Response after token verification."""
    valid: bool
    role: UserRole
    message: Optional[str] = None


class AuthStatus(BaseModel):
    """Current authentication status."""
    authenticated: bool
    role: UserRole
