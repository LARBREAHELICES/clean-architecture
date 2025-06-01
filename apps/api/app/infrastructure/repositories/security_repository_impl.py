from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, MutableMapping

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.domain.interfaces.SecurityServiceProtocol import SecurityServiceProtocol
from app.config.dev import settings

# Configuration sécurisée (à externaliser et protéger)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityRepositoryImp(SecurityServiceProtocol):
    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, subject: str, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode: MutableMapping[str, Any] = {
            "sub": subject,
            "exp": int(expire.timestamp())
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            return payload
        except JWTError as e:
            # Tu peux aussi créer une exception métier spécifique ici
            raise ValueError("Invalid token") from e
        
    def create_refresh_token(self, subject: str, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(days=7))
        to_encode : MutableMapping[str, Any] = {"sub": subject, "exp": int(expire.timestamp())}
        
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
