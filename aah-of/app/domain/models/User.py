
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class BaseUser:
    id: Optional[str] 
    username: str
    bonus: int
    email: Optional[str] = None

@dataclass
class User(BaseUser):
    pass

@dataclass
class UserAuth(BaseUser):
    password: str
    is_active: bool = False
    

@dataclass
class UserTerms(BaseUser):
    terms: List["Term"]