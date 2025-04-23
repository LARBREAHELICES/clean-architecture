from sqlmodel import Session
from typing import List
from app.domain.models.user import User
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol as UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def list_users(self) -> List[User]:
        return self.session.query(User).all()
