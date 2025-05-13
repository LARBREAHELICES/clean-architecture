from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from fastapi import  Depends

from typing import List
from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.models.User_Term_DB import User_Term_DB
from app.infrastructure.db.models.TermDB import TermDB

from app.infrastructure.db.mappers.user_mapper import UserMapper
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol

from app.infrastructure.db.database import get_db

"""
L'infrastructure implémente l'interface et fait concrètement les requêtes
"""
class UserRepositoryImpl(UserServiceProtocol):
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_user(self, user_db: UserDB) -> UserDB:
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        
        return user_db

    def list_users(self) -> List[UserDB]:
        users_db = self.session.query(UserDB).all() # SQLModel
        
        return [UserMapper.to_domain(user_db) for user_db in users_db] # mapping
    
    def get_user_by_id(self, user_id: int) -> UserDB | None:
        user_db = self.session.query(UserDB).where(UserDB.id == user_id).first()
        if user_db is None:
            return None
        
        return user_db
    
    def get_user_with_terms(self, user_id: int) -> UserDB | None:
        statement = (
            select(UserDB)
            .where(UserDB.id == user_id)
            .options(selectinload(UserDB.terms))  # charge les terms liés
        )
        
        user_db = self.session.exec(statement).one_or_none()

        if user_db is None:
            return None

        return user_db
    
    def assign_user_terms(self, user: UserDB, terms: List[TermDB]) -> UserDB:
        for term in terms:
            link = User_Term_DB(user_id=user.id, term_id=term.id)
            self.session.add(link)
        
        self.session.commit()
        
        return self.get_user_with_terms(user.id)
    
    def get_users_by_term(self, term_id: int) -> List[UserDB]:
        statement = (
            select(UserDB)
            .join(User_Term_DB, User_Term_DB.user_id == UserDB.id)
            .where(User_Term_DB.term_id == term_id)
            .options(selectinload(UserDB.terms))
        )
        results = self.session.exec(statement).all()
        
        return [user_db for user_db in results]