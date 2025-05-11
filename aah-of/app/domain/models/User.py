
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class BaseUser:
    username: str
    bonus: int
    email: str
    id: Optional[int] 
    disabled: bool = False
    password: str

@dataclass
class User(BaseUser):
    pass

@dataclass
class UserCreate:
    username: str
    bonus: int
    email: str
    password: str

@dataclass
class UserTerms(BaseUser):
    terms: List["Term"]