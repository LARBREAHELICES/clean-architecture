from typing import Protocol, runtime_checkable
from app.domain.models.Term import Term
from app.domain.models.User import User
from typing import List

"""
Comportement utiliser par le domaine => 3 méthodes à implémenter 
Pas de dépendances avec l'infrastructure 
"""

@runtime_checkable
class TermServiceProtocol(Protocol):
    def create_term(self, user: Term) -> Term:
        ...
    def get_term_by_id(self, user_id: int) -> Term | None:
        ...
    
    def list_terms(self) -> List[Term]:
        ...
    
    def get_users_for_term(self)-> list[User]:
        ...