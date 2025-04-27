from sqlmodel import Session

from typing import List
from app.domain.models.User import User
from app.infrastructure.db.models.UserDB import UserDB
from app.infrastructure.db.mappers.user_mapper import UserMapper
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
from app.infrastructure.db.mappers.user_response_mapper import UserReponseMapper

"""
L'infrastructure implémente l'interface et fait concrètement les requêtes
"""
class UserRepositoryImpl(UserServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        user_db = UserMapper.to_db(user) # UserDB
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        
        return UserMapper.to_domain(user_db)

    def list_users(self) -> List[User]:
        users_db = self.session.query(UserDB).all() # SQLModel
        
        return [UserMapper.to_domain(user_db) for user_db in users_db] # mapping
    
    def get_user_by_id(self, user_id: int) -> User | None:
        user_db = self.session.query(UserDB).where(UserDB.id == user_id).first()
        if user_db is None:
            return None
        
        return UserMapper.to_domain(user_db)
    
    def get_user_by_id_with_terms(self, user_id: int):
        user_db = self.session.query(UserDB).where(UserDB.id == user_id).first()
        
        return UserReponseMapper.to_domain(user_db) 

    