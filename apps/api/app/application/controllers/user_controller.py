from typing import List

from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService
from app.application.usecases.assign_terms_to_user import AssignTermsToUserUseCase
from app.application.usecases.register.create_user import CreateUserUseCase

from app.application.mappers.user_mapper import (
    domain_to_dto_user,
    domain_to_dto_user_with_terms,
)
from app.application.dtos.user_dto import UserDTO, UserCreateDTO, UserWithTermsDTO

class UserController:
    def __init__(
        self,
        user_service: UserService,
        term_service: TermService,
        assign_terms_uc: AssignTermsToUserUseCase,
        create_user_uc: CreateUserUseCase
    ):
        self.user_service = user_service
        self.term_service = term_service
        self.assign_terms_uc = assign_terms_uc
        self.create_user_uc = create_user_uc

    def create_user(self, user_create_dto: UserCreateDTO) -> UserDTO:
        user_domain = self.create_user_uc.execute(user_create_dto)
        
        return domain_to_dto_user(user_domain)

    def get_user_by_id(self, user_id: str) -> UserDTO:
        user_domain = self.user_service.get_user_by_id(user_id)
        
        return domain_to_dto_user(user_domain)

    def list_users(self) -> List[UserDTO]:
        users_domain = self.user_service.list_users()
        
        return [domain_to_dto_user(user) for user in users_domain]

    def add_term_to_user(self, user_id: str, term_id: str) -> UserDTO:
        self.term_service.add_term_to_user(user_id, term_id)
        updated_user_domain = self.user_service.get_user_by_id(user_id)
        
        return domain_to_dto_user(updated_user_domain)

    def get_user_with_terms(self, user_id: str) -> UserWithTermsDTO:
        user_terms_domain = self.user_service.get_user_with_terms(user_id)
        
        return domain_to_dto_user_with_terms(user_terms_domain)

    def assign_terms_to_user(self, user_id: str, term_ids: List[str]) -> UserWithTermsDTO:
        user_terms_domain = self.assign_terms_uc.execute(user_id, term_ids)
        
        return domain_to_dto_user_with_terms(user_terms_domain)

    def get_users_by_term(self, term_id: str) -> List[UserDTO]:
        users_domain = self.user_service.get_users_by_term(term_id)
        
        return [domain_to_dto_user(user) for user in users_domain]
