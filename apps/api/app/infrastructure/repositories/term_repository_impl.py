from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.domain.models.Term import Term, TermUsers
from app.domain.models.User import User
from app.infrastructure.db.models.TermDB import TermDB

class TermRepositoryImpl(TermServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create_term(self, term: Term) -> Term:
        term_db = TermDB(**term.model_dump(exclude_unset=True))
        self.session.add(term_db)
        self.session.commit()
        self.session.refresh(term_db)

        return Term(id=term_db.id, name=term_db.name)

    def get_term_by_id(self, term_id: str) -> Optional[Term]:
        term_db = self.session.get(TermDB, term_id)
        if not term_db:
            return None
        return Term(id=term_db.id, name=term_db.name)

    def list_terms(self) -> List[Term]:
        terms_db = self.session.query(TermDB).all()
        return [Term(id=term.id, name=term.name) for term in terms_db]

    def get_users_for_term(self, term_id: str) -> Optional[TermUsers]:
        statement = (
            select(TermDB)
            .where(TermDB.id == term_id)
            .options(selectinload(TermDB.users))
        )
        term_db = self.session.exec(statement).one_or_none()
        if not term_db:
            return None

        return TermWithUsers(
            id=term_db.id,
            name=term_db.name,
            users=[
                User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    bonus=user.bonus,
                    is_active=user.is_active
                )
                for user in term_db.users or []
            ]
        )
