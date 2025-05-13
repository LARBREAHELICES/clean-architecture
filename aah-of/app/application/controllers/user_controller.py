from typing import List

from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService
from app.application.usecases.assign_terms_to_user import AssignTermsToUserUseCase

from app.domain.dtos.user_dto import UserDTO, UserWithTermsDTO, UserCreateDTO

class UserController:
    def __init__(
        self,
        user_service: UserService,
        term_service: TermService,
        assign_terms_uc: AssignTermsToUserUseCase
    ):
        self.user_service = user_service
        self.term_service = term_service
        self.assign_terms_uc = assign_terms_uc

    def create_user(self, user: UserCreateDTO) -> UserDTO:
        user = self.user_service.create_user(user)
        # Tu transformes un objet SQLAlchemy (UserDB) ici userDB
        # en objet Pydantic (UserResponse), que tu peux retourner dans une réponse FastAPI.
        return UserDTO.from_orm(user) 

    def get_user_by_id(self, user_id: str) -> UserDTO:
        user = self.user_service.get_user_by_id(user_id)
        
        return UserDTO.model_validate(user)

    def list_users(self) -> List[UserDTO]:
        users = self.user_service.list_users()
        
        return [UserDTO.model_validate(user) for user in users]

    def add_term_to_user(self, user_id: str, term_id: str) -> UserDTO:
        self.term_service.add_term_to_user(user_id, term_id)
        updated_user = self.user_service.get_user_by_id(user_id)
        
        return UserDTO.model_validate(updated_user)

    def get_user_with_terms(self, user_id: str) -> UserWithTermsDTO:
        user_temrs = self.user_service.get_user_with_terms(user_id)
        
        return UserWithTermsDTO.model_validate(user_temrs)

    def assign_terms_to_user(self, user_id: str, term_ids: List[str]) -> UserWithTermsDTO:
        user_terms = self.assign_terms_uc.execute(user_id, term_ids)
        
        return UserWithTermsDTO.model_validate(user_terms)

    def get_users_by_term(self, term_id: str) -> List[UserDTO]:
        users = self.user_service.get_users_by_term(term_id)
        
        return [UserDTO.model_validate(user) for user in users]
