from typing import Protocol
from app.domain.models.user import User
from typing import List

"""
Comportement utiliser par le domaine => 3 méthodes à implémenter 
Pas de dépendances avec l'infrastructure 
"""

class UserServiceProtocol(Protocol):
    def create_user(self, user: User) -> User:
        ...
    
    def get_user_by_id(self, user_id: int) -> User | None:
        ...
    
    def list_users(self) -> List[User]:
        ...
        
    def get_users_by_category(self, category: str) -> List[User]:
        ...