from typing import Protocol, runtime_checkable
from app.domain.models.User import User, UserTerms, UserWithPassword
from app.domain.models.Term import Term
from typing import List

"""
Comportement utiliser par le domaine => 3 méthodes à implémenter 
Pas de dépendances avec l'infrastructure 
"""

@runtime_checkable
class UserServiceProtocol(Protocol):
    def create_user(self, user: UserWithPassword) -> User:
        ...
    
    def get_user_by_id(self, user_id: str) -> User | None:
        ...
    
    def list_users(self) -> List[User]:
        ...
        
    def get_user_by_username(self, username: str) -> User | None:
        ...
    
    def get_user_by_username_with_password(self, username: str) -> UserWithPassword | None:
        ...
        
    def get_user_with_terms(self, user_id : str) -> UserTerms | None:
        ...
    
    def assign_user_terms(self,user: User, terms: List[Term] )->UserTerms | None:
        ...
        
    def get_users_by_term(self, term_id: str) -> List[UserTerms]:
        ...