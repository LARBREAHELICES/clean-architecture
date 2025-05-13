
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class BaseUser:
    id: Optional[str] 
    username: str
    bonus: int

@dataclass
class User(BaseUser):
    pass

@dataclass
class UserTerms(BaseUser):
    terms: List["Term"]