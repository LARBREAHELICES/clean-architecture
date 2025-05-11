from dataclasses import dataclass
from typing import List


@dataclass
class Term:
    id: int
    name: str
    
@dataclass
class TermUsers:
    id: int
    name: str
    users : List