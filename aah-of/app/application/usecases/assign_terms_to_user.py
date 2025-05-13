from app.domain.models.Term import Term
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol

from app.domain.dtos.user_dto import UserWithTermsDTO

class AssignTermsToUserUseCase:
    def __init__(
        self,
        user_service: UserServiceProtocol,
        term_service: TermServiceProtocol
    ):
        self.user_service = user_service
        self.term_service = term_service

    def execute(self, user_id: int, term_ids: list[int]) -> UserWithTermsDTO:
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found.")

        terms: list[Term] = []
        for term_id in term_ids:
            term = self.term_service.get_term_by_id(term_id)
            if not term:
                raise ValueError(f"Term {term_id} not found.")
            terms.append(term)

        return self.user_service.assign_user_terms(user, terms)
        