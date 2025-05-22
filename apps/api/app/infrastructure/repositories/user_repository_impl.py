from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB

from app.domain.models.User import User, UserTerms, UserWithPassword
from app.domain.models.Term import Term

from app.application.mappers.user_mapper import orm_to_domain_user, orm_to_domain_user_with_password, domain_to_dto_user_with_terms

class UserRepositoryImpl:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        user_db = UserDB(**user.model_dump())  # Conversion domaine -> ORM via dump
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        
        return orm_to_domain_user(user_db)  # Mapper ORM -> domaine

    def list_users(self) -> List[User]:
        users_db = self.session.query(UserDB).all()
        
        return [orm_to_domain_user(user_db) for user_db in users_db]

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        user_db = self.session.query(UserDB).filter(UserDB.id == user_id).first()
        if not user_db:
            return None
        
        return orm_to_domain_user(user_db)

    def get_user_by_username(self, username: str) -> Optional[User]:
        user_db = self.session.query(UserDB).filter(UserDB.username == username).first()
        if not user_db:
            return None
        
        return orm_to_domain_user(user_db)

    def get_user_by_username_with_password(self, username: str) -> Optional[UserWithPassword]:
        user_db = self.session.query(UserDB).filter(UserDB.username == username).first()
        if not user_db:
            return None
        
        return orm_to_domain_user_with_password(user_db)

    def get_user_with_terms(self, user_id: str) -> Optional[UserTerms]:
        statement = (
            select(UserDB)
            .where(UserDB.id == user_id)
            .options(selectinload(UserDB.terms))
        )
        user_db = self.session.exec(statement).one_or_none()
        if not user_db:
            return None
        
        return domain_to_dto_user_with_terms(user_db)

    def assign_user_terms(self, user: User, terms: List[Term]) -> Optional[UserTerms]:
        for term in terms:
            link = User_Term_DB(user_id=user.id, term_id=term.id)
            self.session.add(link)
        self.session.commit()

        return self.get_user_with_terms(user.id)

    def get_users_by_term(self, term_id: str) -> List[UserTerms]:
        statement = (
            select(UserDB)
            .join(User_Term_DB, User_Term_DB.user_id == UserDB.id)
            .where(User_Term_DB.term_id == term_id)
            .options(selectinload(UserDB.terms))
        )
        users_db = self.session.exec(statement).all()
        
        return [self.get_user_with_terms(user.id) for user in users_db]
