# app/application/mappers/term_mapper.py

from app.infrastructure.db.models.TermDB import TermDB
from app.domain.models.Term import Term
from app.application.dtos.term_dto import TermDTO

def orm_to_domain_term(term_db: TermDB) -> Term:
    
    return Term(**term_db.model_dump())

def domain_to_dto_term(term: Term) -> TermDTO:
    
    return TermDTO.model_validate(term)