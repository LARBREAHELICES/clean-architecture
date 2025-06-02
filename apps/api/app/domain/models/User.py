
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Permission:
    id: Optional[str]
    name: str  # ex : "view_trainer_availability"

@dataclass
class Role:
    id: Optional[str]
    name: str  # ex : "admin", "trainer", "manager"
    permissions: Optional[List[Permission] ]

@dataclass
class BaseUser:
    username: str
    bonus: int
    email: str
    is_active: bool
    role: Optional[Role]  

@dataclass
class User(BaseUser):
    id: Optional[str] 

@dataclass
class UserCreate(BaseUser):
    pass
    
@dataclass
class UserWithPassword(BaseUser):
    password: str
    
@dataclass
class UserwithoutPassword(BaseUser):
    pass

@dataclass
class UserTerms(BaseUser):
    id: Optional[str] 
    terms: List["Term"]
    