
from dataclasses import dataclass
from typing import Optional, List

from app.domain.models.Term import Term

@dataclass
class UserResponse:
    id: Optional[int]
    username: str
    bonus: int
    terms : List[Term]
