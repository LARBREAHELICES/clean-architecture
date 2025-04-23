from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.models.user import User

# tu hérites de UserServiceProtocol qui est l'interface
class UserService:
    def __init__(self, user_repository: UserServiceProtocol):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.user_repository.list_users()
    
    def sum_bonus(self, coeff : float = 1.1) -> int:
        # logique métier on augmente de 10% les bonus
        return sum( user.bonus*coeff for user in self.list_users()) 
