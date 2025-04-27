from typing import Protocol
from app.domain.models.Term import Term
from typing import List

"""
Comportement utiliser par le domaine => 3 méthodes à implémenter 
Pas de dépendances avec l'infrastructure 
"""

class TermServiceProtocol(Protocol):
    def create_term(self, user: Term) -> Term:
        ...
    def get_term_by_id(self, user_id: int) -> Term | None:
        ...
    
    def list_terms(self) -> List[Term]:
        ...
    
    def add_term_to_user(self, user_id: int, term_id: int) -> None:
        """Associe un terme à un utilisateur"""
        ...