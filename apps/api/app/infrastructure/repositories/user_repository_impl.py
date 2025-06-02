from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List

from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.RoleDB import RoleDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.domain.models.User import User, UserTerms, UserWithPassword, Role, Permission
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
            is_active=user_db.is_active,
            role=user_db.role
        )

    def list_users(self) -> List[User]:
        statement = select(UserDB).options(
            selectinload(UserDB.role).selectinload(RoleDB.permissions)
        )
        users = self.session.exec(statement).all()
        
        print(users)
        return [
            User(
                id=user.id,
                username=user.username,
                email=user.email,
                bonus=user.bonus,
                is_active=user.is_active,
                role= Role(
                id=user.role.id,
                name=user.role.name,
                permissions=[Permission(id=p.id, name=p.name) for p in user.role.permissions] if user.role and user.role.permissions else []
            )
            ) for user in users
        ]

    def get_user_by_id(self, user_id: str) -> User | None:
        statement = (
            select(UserDB)
            .where(UserDB.id == user_id)
            .options(selectinload(UserDB.role).selectinload(RoleDB.permissions))
        )
        user = self.session.exec(statement).first()
        if not user:
            return None
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active,
            role= Role(
                id=user.role.id,
                name=user.role.name,
                permissions=[Permission(id=p.id, name=p.name) for p in user.role.permissions] if user.role and user.role.permissions else []
            )
        )

    def get_user_by_username(self, username: str) -> User | None:
        statement = (
            select(UserDB)
            .where(UserDB.username == username)
            .options(selectinload(UserDB.role).selectinload(RoleDB.permissions))
        )
        user = self.session.exec(statement).first()
        if not user:
            return None
        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active,
            role= user.role
        )

    def get_user_by_username_with_password(self, username: str) -> UserWithPassword | None:
        statement = (
            select(UserDB)
            .where(UserDB.username == username)
            .options(selectinload(UserDB.role).selectinload(RoleDB.permissions))
        )
        user = self.session.exec(statement).first()
        if not user:
            return None
        return UserWithPassword(
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active,
            password=user.password,
            role= Role(
                id=user.role.id,
                name=user.role.name,
                permissions=[Permission(id=p.id, name=p.name) for p in user.role.permissions] if user.role and user.role.permissions else []
            )
        )

    def get_user_with_terms(self, user_id: str) -> UserTerms | None:
        statement = (
            select(UserDB)
            .where(UserDB.id == user_id)
            .options(
                selectinload(UserDB.terms),
                selectinload(UserDB.role).selectinload(RoleDB.permissions)
            )
        )
        user = self.session.exec(statement).first()
        if not user:
            return None

        return UserTerms(
            id=user.id,
            username=user.username,
            email=user.email,
            bonus=user.bonus,
            is_active=user.is_active,
             role= Role(
                id=user.role.id,
                name=user.role.name,
                permissions=[Permission(id=p.id, name=p.name) for p in user.role.permissions] if user.role and user.role.permissions else []
            ),
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
        if user is None:
            return None
        
        return self.get_user_with_terms(user.id)

    def get_users_by_term(self, term_id: str) -> List[UserTerms]:
        statement = (
            select(UserDB)
            .join(User_Term_DB, User_Term_DB.user_id == UserDB.id)
            .where(User_Term_DB.term_id == term_id)
            .options(
                selectinload(UserDB.terms),
                selectinload(UserDB.role).selectinload(RoleDB.permissions)
            )
        )
        users = self.session.exec(statement).all()
        
        if not users:
            return []

        return [
            self.get_user_with_terms(user.id)
            for user in users if user is not None
        ]
