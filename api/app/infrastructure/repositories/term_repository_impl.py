from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.domain.models.Term import Term

from app.infrastructure.db.models.TermDB import TermDB
from app.infrastructure.db.models.UserDB import UserDB

from app.infrastructure.db.mappers.term_mapper import TermMapper

from typing import List
from sqlmodel import Session

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

    def add_term_to_user(self, user_id: int, term_id: int) -> None:
        user_db = self.session.get(UserDB, user_id)
        term_db = self.session.get(TermDB, term_id)
        
        if user_db and term_db:
            user_db.terms.append(term_db)
            self.session.commit()
        else:
            raise ValueError("Utilisateur ou terme non trouvé")
