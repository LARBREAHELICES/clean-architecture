# app/controllers/user_controller.py
from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService
from app.application.usecases.assign_terms_to_user import AssignTermsToUserUseCase

from app.api.schemas.user_schema import UserCreateRequest, UserResponse, UserTermResponse
from app.application.usecases.mappers.user_mapper import UserMapper

from typing import List

class UserController:
    def __init__(self,
                 user_service : UserService, 
                 term_service : TermService,
                 assign_terms_uc : AssignTermsToUserUseCase 
    ):
        
        self.user_service = user_service
        self.term_service = term_service
        self.assign_terms_uc = assign_terms_uc
    
    def create_user(self, user: UserCreateRequest) -> UserResponse:
        user_domain = UserMapper.from_request(user)
        created_user = self.user_service.create_user(user_domain)
        
        return UserMapper.to_response(created_user)
    
    def get_user_by_id(self, user_id: int) -> UserResponse:
        
        user = self.user_service.get_user_by_id(user_id)
        
        return UserMapper.to_response(user) 
    
    def list_users(self) -> List[UserResponse]:
        
        users = self.user_service.list_users()
        
        return [UserMapper.to_response(user) for user in users]
        
    def add_term_to_user(self, user_id: int, term_id: int) -> UserResponse:
        
        user = self.user_service.get_user_by_id(user_id)
        if user:
            self.term_service.add_term_to_user(user_id, term_id)
        
        return  UserMapper.to_response(user)

    def get_user_with_terms(self, user_id: int) -> UserTermResponse:
        userterms = self.user_service.get_user_with_terms(user_id)
        
        return UserMapper.to_userterms_response(userterms)
    
    def assign_terms_to_user(self, user_id: int, term_ids: List[int])-> UserTermResponse:
        
        userterms = self.assign_terms_uc.execute(user_id, term_ids)
    
        return UserMapper.to_userterms_response(userterms)
    
    def get_users_by_term(self, term_id: int) -> List[UserResponse]:
        users = self.user_service.get_users_by_term(term_id)
        
        return [UserMapper.to_response(user) for user in users]