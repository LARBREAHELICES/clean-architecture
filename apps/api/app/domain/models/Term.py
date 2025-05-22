from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

@dataclass
class BaseTerm:
    id: Optional[UUID] 
    name: str

@dataclass
class Term(BaseTerm):
    pass

@dataclass
class TermUsers(BaseTerm):
    users: List["User"]
