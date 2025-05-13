# app/controllers/term_controller.py
from app.domain.services.term_service import TermService
from app.domain.models.Term import Term

# sérialisation API schema FastAPI
from app.api.schemas.term_schema import TermCreateRequest, TermResponse
from app.application.usecases.mappers.term_mapper import TermMapper

from typing import List

class TermController:
    def __init__(self):
        self.term_service =TermService
    
    def list_term(self, term_id: int) -> TermResponse | None:
        term = self.term_service.get_term_by_id(term_id)
        
        return TermMapper.to_response(term)
    
    def list_terms(self) -> List[Term]:
        terms = self.term_service.list_terms()
        
        return  [TermMapper.to_response(term) for term in terms]

    def create_term(self, term: TermCreateRequest) -> TermResponse:
        term_domain = TermMapper.from_request(term)
        created_term =  self.term_service.create_term(term_domain)
        
        return TermMapper.to_response(created_term)
