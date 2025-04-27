# app/controllers/user_controller.py
from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl

from sqlmodel import Session
from app.domain.models.User import User
from app.domain.models.UserResponse import UserResponse
from app.domain.models.Term import Term

from app.infrastructure.db.schemas.user_schema import UserCreateRequest

from typing import List

class UserController:
    def __init__(self, db: Session):
        self.db = db
        
        self.user_repository = UserRepositoryImpl(db)
        self.user_service = UserService(self.user_repository)
        
        self.term_repository = TermRepositoryImpl(db)
        self.term_service = TermService(self.term_repository)
    
    def create_user(self, user: UserCreateRequest) -> User:
        
        return self.user_service.create_user(user)
    
    def get_user_by_id(self, user_id: int) -> User:
        
        return self.user_service.get_user_by_id(user_id)
    
    def list_users(self) -> List[User]:
        
        return self.user_service.list_users()
    
    def add_term_to_user(self, user_id: int, term_id: int) -> User:
        
        user = self.user_service.get_user_by_id(user_id)
        if user:
            self.term_service.add_term_to_user(user_id, term_id)
        return user

    def list_terms_for_user(self, user_id: int)-> UserResponse:
        
        return self.user_service.list_terms_for_user(user_id)