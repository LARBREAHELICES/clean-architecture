# app/application/mappers/term_mapper.py

from app.infrastructure.db.models.TermDB import TermDB
from app.domain.models.Term import Term
from app.application.dtos.term_dto import TermDTO

def orm_to_domain_term(term_db: TermDB) -> Term:

    if not term_db.id:
        return Term(id=None, name=term_db.name)
    
    return Term(id=term_db.id, name=term_db.name)

def domain_to_term_dto(term: Term) -> TermDTO:
    
    return TermDTO(id=term.id, name=term.name)