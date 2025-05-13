from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import Depends
from typing import List

from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB
from app.infrastructure.db.models.TermDB import TermDB

from app.domain.dtos.user_dto import UserDTO, UserWithTermsDTO
from app.domain.dtos.term_dto import TermDTO

from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.infrastructure.db.database import get_db

from app.domain.models.User import User, UserTerms
from app.domain.models.Term import Term

class UserRepositoryImpl(UserServiceProtocol):
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_user(self, user: User) -> User:
        user_db = UserDB(**user.model_dump())
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        
        user_dto = UserDTO.from_orm(user_db)
        
        return User(**user_dto.__dict__)

    def list_users(self) -> List[User]:
        users = self.session.query(UserDB).all()
        
        return [User(**UserDTO.from_orm(user_db).__dict__) for user_db in users]

    def get_user_by_id(self, user_id: int) -> User | None:
        user_db = self.session.query(UserDB).where(UserDB.id == user_id).first()
        if not user_db:
            return None
        user_dto = UserDTO.from_orm(user_db)
        
        return User(**user_dto.__dict__)

    def get_user_with_terms(self, user_id: int) -> UserTerms | None:
        statement = (
            select(UserDB)
            .where(UserDB.id == user_id)
            .options(selectinload(UserDB.terms))
        )
        user_db = self.session.exec(statement).one_or_none()

        if not user_db:
            return None
        
        # Convertir d'abord l'ORM en DTO, puis DTO en modèle métier
        user_dto = UserDTO.from_orm(user_db)
        
        return UserTerms(
            **user_dto.dict(),  # Utilisation de dict() au lieu de __dict__
            terms=[
            Term(**TermDTO.from_orm(term_db).dict()) for term_db in user_db.terms or []
        ]
    )

    def assign_user_terms(self, user: User, terms: List[Term]) -> UserTerms | None:
        for term in terms:
            self.session.add(User_Term_DB(user_id=user.id, term_id=term.id))
        self.session.commit()

        return self.get_user_with_terms(user.id)

    def get_users_by_term(self, term_id: int) -> List[UserTerms]:
        statement = (
            select(UserDB)
            .join(User_Term_DB, User_Term_DB.user_id == UserDB.id)
            .where(User_Term_DB.term_id == term_id)
            .options(selectinload(UserDB.terms))
        )
        users = self.session.exec(statement).all()

        return [
            self.get_user_with_terms(user.id)
            for user in users
        ]
