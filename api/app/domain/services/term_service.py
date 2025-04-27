# app/domain/services/TermService.py
from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.domain.models.Term import Term
from app.domain.models.User import User
from typing import List

class TermService:
    def __init__(self, term_repository: TermServiceProtocol):
        self.term_repository = term_repository

    def create_term(self, term: Term) -> Term:
        return self.term_repository.create_term(term)

    def get_term_by_id(self, term_id: int) -> Term | None:
        return self.term_repository.get_term_by_id(term_id)

    def list_terms(self) -> List[Term]:
        return self.term_repository.list_terms()

    def add_term_to_user(self, user_id: int, term_id: int) -> None:
        """Ajoute un terme à un utilisateur"""
        return self.term_repository.add_term_to_user(user_id, term_id)
