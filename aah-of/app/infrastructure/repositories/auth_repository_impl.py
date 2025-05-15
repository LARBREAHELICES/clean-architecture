from app.domain.interfaces.AuthServiceProtocol import AuthServiceProtocol
from app.domain.models.User import User

from passlib.context import CryptContext
from jose import JWTError, jwt
from app.domain.models.User import User
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl  # dépend de ton infra
from app.config import settings  # contient secret, algo, etc
from fastapi import HTTPException, status

class AuthRepository(AuthServiceProtocol):
    def __init__(self, user_repo: UserRepositoryImpl):
        self.user_repo = user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def authenticate(self, username: str, password: str) -> bool:
        user = self.user_repo.get_user_by_username(username)
        if not user:
            return False
        
        return self.pwd_context.verify(password, user.hashed_password)
    
    def get_user_from_token(self, token: str) -> User:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = self.user_repo.get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    
    def ensure_user_is_active(self, user: User) -> User:
        pass