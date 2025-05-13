from dataclasses import dataclass
from typing import List, Optional

@dataclass
class BaseTerm:
    id: Optional[str] 
    name: str

@dataclass
class Term(BaseTerm):
    pass

@dataclass
class TermUsers(BaseTerm):
    users: List["User"]
