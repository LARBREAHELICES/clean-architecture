# app/application/mappers/user_mapper.py

from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

from app.domain.models.User import User, UserTerms, UserWithPassword
from app.infrastructure.db.models.UserDB import UserDB
from app.application.mappers.term_mapper import orm_to_domain_term
from app.application.dtos.user_dto import UserDTO, UserCreateDTO, UserWithTermsDTO
from app.application.dtos.term_dto import TermDTO
from app.application.mappers.term_mapper import domain_to_dto_term

def dto_to_domain_user(dto: UserDTO) -> User:
    
    return User(**dto.dict())

def domain_to_dto_user(user: User) -> UserDTO | None:
    if not user:
        return None
    
    return UserDTO(**user.__dict__)

def orm_to_domain_user(user_db: UserDB) -> User:
    
    return User(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email,
        bonus=user_db.bonus,
        is_active=user_db.is_active
    )

def orm_to_domain_user_terms(user_db: UserDB) -> UserTerms:
    
    return UserTerms(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email,
        bonus=user_db.bonus,
        is_active=user_db.is_active,
        terms=[orm_to_domain_term(term) for term in user_db.terms]
    )

def orm_to_domain_user_with_password(user_db: UserDB) -> UserWithPassword:
    # On crée un DTO de création (UserCreateDTO) depuis l'ORM
    user_create_dto = UserCreateDTO.from_orm(user_db)
    # Puis on instancie le modèle domaine avec les données du DTO
    return UserWithPassword(**user_create_dto.dict())

def domain_to_dto_user_with_terms(user: UserTerms) -> UserWithTermsDTO | None:
    if not user:
        return None
    terms_dto = [domain_to_dto_term(term) for term in (user.terms or [])]
    return UserWithTermsDTO(
        id=user.id,
        username=user.username,
        bonus=user.bonus,
        email=user.email or "",  # éviter None ici si nécessaire
        is_active=user.is_active,
        terms=terms_dto
    )
    
def orm_to_domain_user_with_password(user_db: UserDB) -> UserWithPassword:
    return UserWithPassword(
        username=user_db.username,
        email=user_db.email,
        bonus=user_db.bonus,
        is_active=user_db.is_active,
        password=user_db.password  # ou user_db.password si tu le stockes tel quel
    )