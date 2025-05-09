# Importation des schémas Pydantic utilisés pour les entrées et sorties HTTP
from app.api.schemas.user_schema import UserCreateRequest, UserResponse, UserTermResponse
from app.api.schemas.term_schema import TermResponse

# Importation du modèle métier (domaine)
from app.domain.models.User import User

from typing import List

# Classe utilitaire pour mapper entre les objets du domaine (User) et les schémas Pydantic (API)
class UserMapper:

    @staticmethod
    def from_request(user_req: UserCreateRequest) -> User:
        # Transforme une requête HTTP de création d'utilisateur en un modèle métier User
        return User(id=None, username=user_req.username, bonus=user_req.bonus)

    @staticmethod
    def to_response(user: User) -> UserResponse:
        # Transforme un User du domaine en un schéma de réponse HTTP simple
        return UserResponse(id=user.id, username=user.username, bonus=user.bonus)
    
    @staticmethod
    def to_responses(users: List[User]) -> List[UserResponse]:
        # Transforme une liste d'utilisateurs du domaine en une liste de réponses HTTP
        return [
            UserResponse(id=user.id, username=user.username, bonus=user.bonus)
            for user in users
        ]
    
    @staticmethod
    def to_userterms_response(user: User) -> UserTermResponse:
        # Transforme un User (contenant des termes associés) en un schéma enrichi
        # utilisé pour la sérialisation complète d'un user avec ses terms
        return UserTermResponse(
            id=user.id,
            username=user.username,
            bonus=user.bonus,
            terms=[
                TermResponse(id=term.id, name=term.name)  # chaque terme est aussi transformé
                for term in user.terms
            ]
        )
