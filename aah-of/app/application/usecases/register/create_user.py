from app.domain.models.Term import Term
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol

from app.application.dtos.user_dto import UserDTO

class CreateUserUseCase:
    def __init__(
        self,
        user_service: UserServiceProtocol,
        security : SecurityServiceProtocol
    ):
        self.user_service = user_service,
        self.security = security

    def execute(self, user_id: str, term_ids: list[str]) -> UserDTO | None:
        pass
        