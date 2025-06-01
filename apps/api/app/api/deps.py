from typing import Generator

from sqlalchemy.orm import Session
from fastapi import Depends

from app.infrastructure.db.database import get_db

from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl
from app.infrastructure.repositories.security_repository_impl import SecurityRepositoryImp
from app.infrastructure.repositories.reporting_summary_repository_impl import ReportingSummaryRepositoryImpl

from app.domain.services.user_service import UserService
from app.domain.services.term_service import TermService
from app.domain.services.auth_service import UserAuthService
from app.domain.services.reporting_service import ReportingSummaryService

from app.application.usecases.assign_terms_to_user import AssignTermsToUserUseCase
from app.application.usecases.register.create_user import CreateUserUseCase

from app.application.controllers.user_controller import UserController
from app.application.controllers.term_controller import TermController
from app.application.controllers.auth_controller import AuthController
from app.application.controllers.reporting_summary_controller import ReportingSummaryController


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=db)


def get_user_service(repo: UserRepositoryImpl = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=repo)


def get_term_repository(db: Session = Depends(get_db)) -> TermRepositoryImpl:
    return TermRepositoryImpl(session=db)


def get_term_service(repo: TermRepositoryImpl = Depends(get_term_repository)) -> TermService:
    return TermService(term_repository=repo)


def get_assign_terms_use_case(
    user_service: UserService = Depends(get_user_service),
    term_service: TermService = Depends(get_term_service),
) -> AssignTermsToUserUseCase:
    return AssignTermsToUserUseCase(
        user_service=user_service,
        term_service=term_service,
    )


def get_security_service() -> SecurityRepositoryImp:
    return SecurityRepositoryImp()


def get_register_user_use_case(
    user_service: UserService = Depends(get_user_service),
    security: SecurityRepositoryImp = Depends(get_security_service),
) -> CreateUserUseCase:
    return CreateUserUseCase(user_service=user_service, security=security)


def get_user_controller(
    user_service: UserService = Depends(get_user_service),
    term_service: TermService = Depends(get_term_service),
    assign_terms_uc: AssignTermsToUserUseCase = Depends(get_assign_terms_use_case),
    create_user_uc: CreateUserUseCase = Depends(get_register_user_use_case),
) -> UserController:
    return UserController(
        user_service=user_service,
        term_service=term_service,
        assign_terms_uc=assign_terms_uc,
        create_user_uc=create_user_uc,
    )


def get_term_controller(service: TermService = Depends(get_term_service)) -> TermController:
    return TermController(service)


def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repo: UserRepositoryImpl = UserRepositoryImpl(db)
    security: SecurityRepositoryImp = SecurityRepositoryImp()

    auth_service: UserAuthService = UserAuthService(user_repo, security)
    return AuthController(auth_service)


def get_reporting_summary_repository(
    db: Session = Depends(get_db),
) -> ReportingSummaryRepositoryImpl:
    return ReportingSummaryRepositoryImpl(session=db)


def get_reporting_summary_service(
    repo: ReportingSummaryRepositoryImpl = Depends(get_reporting_summary_repository),
) -> ReportingSummaryService:
    return ReportingSummaryService(repository=repo)


def get_reporting_summary_controller(
    service: ReportingSummaryService = Depends(get_reporting_summary_service),
) -> ReportingSummaryController:
    return ReportingSummaryController(service)
