from app.infrastructure.db.database import get_db

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl

from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService

from app.application.usecases.assign_terms_to_user import AssignTermsToUserUseCase
from app.application.controllers.user_controller import UserController
from app.application.controllers.term_controller import TermController

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.security_repositroy_impl import SecurityRepositoryImp
from app.domain.services.auth_service import UserAuthService
from app.application.controllers.auth_controller import AuthController

from sqlalchemy.orm import Session
from fastapi import Depends

def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=db)

def get_user_service(repo: UserRepositoryImpl = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=repo)

def get_term_repository(db: Session = Depends(get_db)) -> TermRepositoryImpl:
    return TermRepositoryImpl(session=db)

def get_term_service(repo: TermRepositoryImpl = Depends(get_term_repository)) -> TermService:
    return TermService(term_repository=repo)

def get_register_user_use_case(
    user_service: UserService = Depends(get_user_service),
    term_service: TermService = Depends(get_term_service)) -> AssignTermsToUserUseCase:
    return AssignTermsToUserUseCase(
        user_service=user_service,
        term_service=term_service)

def get_user_controller(
    user_service: UserService = Depends(get_user_service),
    term_service: TermService = Depends(get_term_service),
    assign_terms_uc: AssignTermsToUserUseCase = Depends(get_register_user_use_case),
) -> UserController:
    return UserController(
        user_service=user_service,
        term_service=term_service,
        assign_terms_uc=assign_terms_uc
    )

def get_term_controller(service=Depends(get_term_service)):
    return TermController(service)

def get_security_service():
    return SecurityRepositoryImp()

def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo = UserRepositoryImpl(db)
    security = SecurityRepositoryImp()

    auth_service = UserAuthService(user_repo, security)
    return AuthController(auth_service)
