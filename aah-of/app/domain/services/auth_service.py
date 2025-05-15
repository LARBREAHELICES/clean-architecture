from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol
from app.domain.interfaces.AuthServiceProtocol import AuthServiceProtocol
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol

from app.domain.models.User import User, UserwithoutPassword

class UserAuthService(AuthServiceProtocol):
    def __init__(
        self, 
        user_service: UserServiceProtocol,
        security: SecurityServiceProtocol
        ):
        self.security = security
        self.user_service = user_service  # simulation, ou repo dans une vraie implémentation

    def authenticate(self, username: str, password: str) -> UserwithoutPassword | None:
        user = self.user_service.get_user_by_username_with_password(username)
        if not user:
            return None
        
        if not self.security.verify_password(password, user.password):
            return None
        
        user_data = user.__dict__.copy()
        user_data.pop("password", None)
        
        return UserwithoutPassword(**user_data)

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
            raise ValueError("Inactive user")
        return user
