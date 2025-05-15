from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol

# Configuration (à externaliser dans un fichier de config ou .env)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityRepositoryImp(SecurityServiceProtocol):
    def hash_password(self, password: str) -> str:
        
        return pwd_context.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        
        return pwd_context.verify(plain, hashed)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as e:
            raise ValueError("Invalid token") from e
