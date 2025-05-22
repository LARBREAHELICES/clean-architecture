from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.application.dtos.term_dto import TermDTO, TermUsersDTO
from app.application.dtos.user_dto import UserDTO

from app.domain.models.Term import Term

from app.infrastructure.db.models.TermDB import TermDB

class TermRepositoryImpl(TermServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create_term(self, term: Term) -> Term:
            
        term_db = TermDB(**term.dict(exclude_unset=True))
        self.session.add(term_db)
        self.session.commit()
        self.session.refresh(term_db)
        
        term_dto = TermDTO.from_orm(term_db)
        
        return Term(**term_dto.__dict__)

    def get_term_by_id(self, term_id: str) -> Optional[TermDTO]:
        term_db = self.session.get(TermDB, term_id)
        if not term_db:
            return None
        return TermDTO.model_validate(term_db)

    def list_terms(self) -> List[TermDTO]:
        terms_db = self.session.query(TermDB).all()
        return [TermDTO.model_validate(term) for term in terms_db]

    def get_users_for_term(self, term_id: str) -> Optional[TermUsersDTO]:
        statement = (
            select(TermDB)
            .where(TermDB.id == term_id)
            .options(selectinload(TermDB.users))
        )
        term_db = self.session.exec(statement).one_or_none()
        if not term_db:
            return None

        return TermUsersDTO(
            id=term_db.id,
            name=term_db.name,
            users=[UserDTO.model_validate(user.__dict__) for user in term_db.users or []]
        )
