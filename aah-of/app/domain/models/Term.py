from dataclasses import dataclass
from typing import List

@dataclass
class BaseTerm:
    id: int
    name: str

@dataclass
class Term(BaseTerm):
    pass

@dataclass
class TermUsers(BaseTerm):
    users: List["User"]
