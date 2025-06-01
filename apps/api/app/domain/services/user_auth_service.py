from typing import Optional
from app.domain.interfaces.AuthServiceProtocol import AuthServiceProtocol
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol
from app.domain.models.User import User, UserwithoutPassword

class UserAuthService(AuthServiceProtocol):
    def __init__(
        self,
        user_service: UserServiceProtocol,
        security: SecurityServiceProtocol
    ):
        self.user_service = user_service
        self.security = security

    def authenticate(self, username: str, password: str) -> Optional[UserwithoutPassword]:
        user = self.user_service.get_user_by_username_with_password(username)
        if not user or not self.security.verify_password(password, user.password):
            return None

        return UserwithoutPassword(
            username=user.username,
            bonus=user.bonus,
            email=user.email,
            is_active=user.is_active
        )

    def get_user_from_token(self, token: str) -> User:
        payload = self.security.decode_token(token)
        username = payload.get("sub")
        if not username:
            raise ValueError("Invalid token")

        user = self.user_service.get_user_by_username(username)
        if not user:
            raise ValueError("User not found")

        return user

    def ensure_user_is_active(self, user: User) -> User:
        if not user.is_active:
            raise ValueError("User inactive")
        return user
