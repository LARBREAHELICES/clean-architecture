from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List

from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.models.User import User, UserTerms, UserWithPassword
from app.domain.models.Term import Term


class UserRepositoryImpl(UserServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        user_db = UserDB(**user.model_dump())
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)

        return User(
            id=user_db.id,
            username=user_db.username,
            email=user_db.email,
            bonus=user_db.bonus,
            is_active=user_db.is_active
        )

    def list_users(self) -> List[User]:
        users = self.session.query(UserDB).all()
        return [
            User(
                id=user.id,
                username=user.username,
                email=user.email,
                bonus=user.bonus,
                is_active=user.is_active
            ) for user in users
        ]

    def get_user_by_id(self, user_id: str) -> User | None:
        user = self.session.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            return None
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active
        )

    def get_user_by_username(self, username: str) -> User | None:
        user = self.session.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            return None
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active
        )

    def get_user_by_username_with_password(self, username: str) -> UserWithPassword | None:
        user = self.session.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            return None
        return UserWithPassword(
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active,
            password=user.password
        )

    def get_user_with_terms(self, user_id: str) -> UserTerms | None:
        statement = (
            select(UserDB)
            .where(UserDB.id == user_id)
            .options(selectinload(UserDB.terms))
        )
        user = self.session.exec(statement).one_or_none()
        if not user:
            return None

        return UserTerms(
            id=user.id,
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active,
            terms=[
                Term(
                    id=term.id,
                    name=term.name
                ) for term in user.terms or []
            ]
        )

    def assign_user_terms(self, user: User, terms: List[Term]) -> UserTerms | None:
        for term in terms:
            self.session.add(User_Term_DB(user_id=user.id, term_id=term.id))
        self.session.commit()
        return self.get_user_with_terms(user.id)

    def get_users_by_term(self, term_id: str) -> List[UserTerms]:
        statement = (
            select(UserDB)
            .join(User_Term_DB, User_Term_DB.user_id == UserDB.id)
            .where(User_Term_DB.term_id == term_id)
            .options(selectinload(UserDB.terms))
        )
        users = self.session.exec(statement).all()
        
        if not users:
            return []

        return [
            self.get_user_with_terms(user.id)
            for user in users if user is not None
        ]
