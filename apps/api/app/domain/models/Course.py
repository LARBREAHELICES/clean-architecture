from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import List

@dataclass
class Course:
    id: UUID
    title: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author_ids: List[UUID]
