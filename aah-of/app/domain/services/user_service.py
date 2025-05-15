from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.models.User import User, UserTerms
from app.domain.models.Term import Term

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

from typing import List

# tu hérites de UserServiceProtocol qui est l'interface
class UserService:
    def __init__(self, user_repository: UserServiceProtocol):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        
        return self.user_repository.create_user(user)

    def get_user_by_id(self, user_id: str) -> User:
        
        return self.user_repository.get_user_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> User:
        
        return self.user_repository.get_user_by_username(username)

    def list_users(self) -> list[User]:
        
        return self.user_repository.list_users()
    
    def sum_bonus(self, coeff : float = 1.1) -> str:
        # logique métier on augmente de 10% les bonus
        return sum( user.bonus*coeff for user in self.list_users()) 
    
    def get_user_with_terms(self, user_id: str) -> UserTerms | None:
        usertems = self.user_repository.get_user_with_terms(user_id)
        
        if not usertems :
            return None
        
        return usertems

    def assign_user_terms(self, user: User, terms: List[Term]) -> UserTerms:
        
        return self.user_repository.assign_user_terms(user, terms)
        
    def get_users_by_term(self, term_id: str) -> List[User]:
        
        return self.user_repository.get_users_by_term(term_id)