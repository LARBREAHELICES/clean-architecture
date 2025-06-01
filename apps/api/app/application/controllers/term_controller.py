from app.domain.services.term_service import TermService
from app.application.dtos.term_dto import TermDTO, TermCreateDTO
from typing import List, Optional

from app.application.mappers.term_mapper import (
    domain_to_term_dto
)

class TermController:
    def __init__(self, term_service: TermService):
        # Injecter le service via le constructeur
        self.term_service = term_service

    def get_term_by_id(self, term_id: str) -> Optional[TermDTO] | None:
        # Récupérer un terme par son ID
        term = self.term_service.get_term_by_id(term_id)
        
        if term:
            return domain_to_term_dto(term)
        return None

    def get_all_terms(self) -> List[TermDTO]:
        # Récupérer la liste des termes
        terms = self.term_service.list_terms()
        
        return [ domain_to_term_dto(term) for term in terms ]

    def create_term(self, term: TermCreateDTO) -> TermDTO:
        # Créer un terme à partir de la requête
        created_term = self.term_service.create_term(term)
        
        return domain_to_term_dto(created_term)
