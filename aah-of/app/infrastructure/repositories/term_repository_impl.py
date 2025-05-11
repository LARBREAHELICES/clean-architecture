from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.domain.models.Term import Term, TermUsers

from app.infrastructure.db.models.TermDB import TermDB
from app.infrastructure.db.models.UserDB import UserDB

from app.infrastructure.db.mappers.term_mapper import TermMapper
from app.infrastructure.db.mappers.user_mapper import UserMapper

from typing import List
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

class TermRepositoryImpl(TermServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create_term(self, term: Term) -> Term:
        term_db = TermMapper.to_db(term) # TermDB
        self.session.add(term_db)
        self.session.commit()
        self.session.refresh(term_db)
        
        return TermMapper.to_domain(term_db)

    def get_term_by_id(self, term_id: int) -> Term | None:
        term_db = self.session.get(TermDB, term_id) # TermDB
        if term_db is None:
            return None
        
        return TermMapper.to_domain(term_db)

    def list_terms(self) -> List[Term]:
        terms_db = self.session.query(TermDB).all()
        
        return [TermMapper.to_domain(term_db) for term_db in terms_db]

    def get_users_for_term(self, term_id: int) -> list[UserDB] | None:
        statement = (
            select(TermDB)
            .where(TermDB.id == term_id)
            .options(selectinload(TermDB.users))  # charge les users liés
        )
        
        term_db = self.session.exec(statement).one_or_none()
        
        if term_db is None:
            return None

        return TermMapper.to_domain_termusers(term_db)
