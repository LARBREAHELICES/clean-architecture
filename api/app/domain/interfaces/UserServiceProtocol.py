from typing import Protocol
from app.domain.models.user import User

class UserServiceProtocol(Protocol):
    def create_user(self, user: User) -> User:
        ...
    
    def get_user_by_id(self, user_id: int) -> User:
        ...
    
    def list_users(self) -> list[User]:
        ...
