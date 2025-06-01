from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol
from app.application.dtos.user_dto import UserDTO, UserCreateDTO

from app.application.mappers.user_mapper import domain_to_dto_user_dto

class CreateUserUseCase:
    def __init__(
        self,
        user_service: UserServiceProtocol,
        security: SecurityServiceProtocol
    ):
        self.user_service = user_service
        self.security = security

    def execute(self, user: UserCreateDTO) -> UserDTO | None:
        # 1. Hachage du mot de passe
        hashed_password = self.security.hash_password(user.password)
        
        # 2. Création de l'utilisateur (enrichi avec le mot de passe hashé)
        user.password = hashed_password
        created_user = self.user_service.create_user(user)

        # 3. Retourne un DTO pour la réponse
        
        return domain_to_dto_user_dto(created_user)