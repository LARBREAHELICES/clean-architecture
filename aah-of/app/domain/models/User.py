
from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

@dataclass
class BaseUser:
    username: str
    bonus: int
    email: str
    is_active: bool

@dataclass
class User(BaseUser):
    id: Optional[str] 

@dataclass
class UserCreate(BaseUser):
    pass
    
@dataclass
class UserWhitPassword(BaseUser):
    password: str
    
@dataclass
class UserwithoutPassword(BaseUser):
    pass

@dataclass
class UserTerms(BaseUser):
    id: Optional[UUID] 
    terms: List["Term"]