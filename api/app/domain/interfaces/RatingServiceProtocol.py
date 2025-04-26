from typing import Protocol, List
from app.domain.models.user import User

"""
Comportement utiliser par le domaine => 2 méthodes à implémenter 
Pas de dépendances avec l'infrastructure 
cela correspond au methode required de l'iterface
"""
class RatingServiceProtocol(Protocol):

    def get_users_by_category(self, category: str) -> List[User]:
        ...