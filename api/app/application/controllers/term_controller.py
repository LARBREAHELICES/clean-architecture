# app/controllers/term_controller.py
from app.domain.services.term_service import TermService
from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl
from sqlmodel import Session
from app.domain.models.Term import Term

# sérialisation API schema FastAPI
from app.infrastructure.db.schemas.term_schema import TermCreateRequest

from typing import List

class TermController:
    def __init__(self, db: Session):
        self.db = db
        self.term_repository = TermRepositoryImpl(db)
        self.term_service = TermService(self.term_repository)
    
    def list_terms(self) -> List[Term]:
        
        return self.term_service.list_terms()
    
    def list_term(self, term_id: int) -> List[Term]:
        
        return self.term_service.get_term_by_id(term_id)
    
    def create_term(self, term: TermCreateRequest) -> Term:
        
        return self.term_service.create_term(term)
