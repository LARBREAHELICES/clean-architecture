from app.domain.services.term_service import TermService
from app.domain.dtos.term_dto import TermDTO, TermCreateDTO
from typing import List, Optional

class TermController:
    def __init__(self, term_service: TermService):
        # Injecter le service via le constructeur
        self.term_service = term_service

    def get_term_by_id(self, term_id: str) -> Optional[TermDTO] | None:
        # Récupérer un terme par son ID
        term = self.term_service.get_term_by_id(term_id)
        
        if term:
            return TermDTO.model_validate(term)
        return None

    def get_all_terms(self) -> List[TermDTO]:
        # Récupérer la liste des termes
        terms = self.term_service.list_terms()
        
        return [ TermDTO.model_validate(term) for term in terms ]

    def create_term(self, term: TermCreateDTO) -> TermDTO:
        # Créer un terme à partir de la requête
        created_term = self.term_service.create_term(term)
        
        return TermDTO.from_orm(created_term)
