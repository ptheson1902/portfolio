"""Authentication service for token validation."""
from ..config import get_settings
from ..models.auth_schemas import UserRole, TokenResponse


class AuthService:
    """Service for authentication operations."""

    def __init__(self):
        self.settings = get_settings()

    def verify_token(self, token: str) -> TokenResponse:
        """
        Verify if a token is valid.
        Currently only supports simple admin token from environment.
        """
        if not token:
            return TokenResponse(
                valid=False,
                role=UserRole.VISITOR,
                message="No token provided"
            )

        # Check against admin token from environment
        if self.settings.admin_token and token == self.settings.admin_token:
            return TokenResponse(
                valid=True,
                role=UserRole.OWNER,
                message="Token verified successfully"
            )

        return TokenResponse(
            valid=False,
            role=UserRole.VISITOR,
            message="Invalid token"
        )

    def get_role_from_token(self, token: str) -> UserRole:
        """Get user role from token."""
        result = self.verify_token(token)
        return result.role


auth_service = AuthService()
