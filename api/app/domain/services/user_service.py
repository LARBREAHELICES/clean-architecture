from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.models.User import User
from app.domain.models.UserResponse import UserResponse
from app.domain.models.Term import Term


from typing import List

# tu hérites de UserServiceProtocol qui est l'interface
class UserService:
    def __init__(self, user_repository: UserServiceProtocol):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.user_repository.list_users()
    
    def sum_bonus(self, coeff : float = 1.1) -> int:
        # logique métier on augmente de 10% les bonus
        return sum( user.bonus*coeff for user in self.list_users()) 
    
    def list_terms_for_user(self, user_id: int) -> UserResponse:
        # Récupérer l'utilisateur et ses termes
        user = self.user_repository.get_user_by_id_with_terms(user_id)
        
        # Retourner un UserResponse avec les termes associés
        return UserResponse(id=user.id, username=user.username, bonus=user.bonus, terms=user.terms)
