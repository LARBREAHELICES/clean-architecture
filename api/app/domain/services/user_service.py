from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository

class UserService(UserServiceProtocol):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.user_repository.list_users()
