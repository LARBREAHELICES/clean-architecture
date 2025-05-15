from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol
from app.domain.interfaces.AuthServiceProtocol import AuthServiceProtocol
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol

from app.domain.models.User import User

class UserAuthService(AuthServiceProtocol):
    def __init__(
        self, 
        security: SecurityServiceProtocol, 
        user_service: UserServiceProtocol 
        ):
        self.security = security
        self.user_service = user_service  # simulation, ou repo dans une vraie implémentation

    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_service.get_user_by_username(username)
        if not user:
            return None
        
        user = User(**user)
        
        if not self.security.verify_password(password, user.password):
            return None
        
        return user

    def get_user_from_token(self, token: str) -> User:
        payload = self.security.decode_token(token)
        username = payload.get("sub")
        if not username:
            raise ValueError("Invalid token")
        user_data = self.users.get(username)
        if not user_data:
            raise ValueError("User not found")
        
        return User(**user_data)

    def ensure_user_is_active(self, user: User) -> User:
        if user.disabled:
            raise ValueError("Inactive user")
        return user
