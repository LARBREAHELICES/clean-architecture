
from sqlmodel import Session, select
from app.domain.models import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user

    def list_users(self) -> list[User]:
        statement = select(User)
        users = self.session.exec(statement).all()
        
        return users