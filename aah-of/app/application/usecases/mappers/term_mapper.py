
from app.api.schemas.term_schema import TermCreateRequest, TermResponse
from app.domain.models.Term import Term

from typing import List

class TermMapper:
    @staticmethod
    def from_request(term_req: TermCreateRequest) -> Term:
        return Term(id=None, name=term_req.name)

    @staticmethod
    def to_response(term: Term) -> TermResponse:
        return TermResponse(id=term.id, name=term.name)
    