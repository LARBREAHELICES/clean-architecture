from typing import Protocol, runtime_checkable
from app.domain.models.User import User
from typing import List

"""
Comportement utiliser par le domaine => 3 méthodes à implémenter 
Pas de dépendances avec l'infrastructure 
"""

@runtime_checkable
class UserServiceProtocol(Protocol):
    def create_user(self, user: User) -> User:
        ...
    
    def get_user_by_id(self, user_id: int) -> User | None:
        ...
    
    def list_users(self) -> List[User]:
        ...
   