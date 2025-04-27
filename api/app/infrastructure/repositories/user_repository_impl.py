from sqlmodel import Session
from typing import List
from app.domain.models.User import User
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol 

"""
L'infrastructure implémente l'interface et fait concrètement les requêtes
"""
class UserRepositoryImpl(UserServiceProtocol):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def list_users(self) -> List[User]:
        return self.session.query(User).all()
    
    def get_user_by_id(self, user_id: int) -> User| None:
        
        return self.session.query(User).where(User.id == user_id).first()
    