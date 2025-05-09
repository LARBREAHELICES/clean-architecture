# app/domain/services/TermService.py
from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.domain.models.Term import Term
from typing import List

class TermService:
    def __init__(self, term_repository: TermServiceProtocol):
        self.term_repository = term_repository

    def create_term(self, term: Term) -> Term:
        # Vérifier des règles métiers avant de créer un terme
        if len(term.name) < 3:
            raise ValueError("Le nom du terme doit être plus long que 3 caractères.")
        
        return self.term_repository.create_term(term)

    def get_term_by_id(self, term_id: int) -> Term | None:
        return self.term_repository.get_term_by_id(term_id)

    def list_terms(self) -> List[Term]:
        return self.term_repository.list_terms()

