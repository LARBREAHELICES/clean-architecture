from typing import List
from app.domain.models.user import User
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol as UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: User) -> User:
        return self.repository.create(user)

    def get_all_users(self) -> List[User]:
        return self.repository.list_users()
