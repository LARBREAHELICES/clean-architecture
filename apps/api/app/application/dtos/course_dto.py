from pydantic import BaseModel

from typing import List
from uuid import UUID
from datetime import datetime

class CourseDTO(BaseModel):
    id: UUID
    title: str
    content: str
    is_published: bool
    created_at: datetime
    updated_at: datetime
    author_ids: List[UUID]

class CreateCourseDTO(BaseModel):
    title: str
    content: str
    author_ids: List[UUID]
