from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.domain.models.Term import Term
from app.domain.models.User import User
from typing import List
from sqlmodel import Session

class TermRepositoryImpl(TermServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create_term(self, term: Term) -> Term:
        self.session.add(term)
        self.session.commit()
        self.session.refresh(term)
        return term

    def get_term_by_id(self, term_id: int) -> Term | None:
        return self.session.get(Term, term_id)

    def list_terms(self) -> List[Term]:
        return self.session.query(Term).all()

    def add_term_to_user(self, user_id: int, term_id: int) -> None:
        user = self.session.get(User, user_id)
        term = self.session.get(Term, term_id)
        
        if user and term:
            user.terms.append(term)
            self.session.commit()
        else:
            raise ValueError("Utilisateur ou terme non trouvé")
