# infrastructure/db/models/course_db.py
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CourseUser(SQLModel, table=True): # type: ignore[misc]
    course_id: UUID = Field(foreign_key="course.id", primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)

class CourseDB(SQLModel, table=True): # type: ignore[misc]
    id: UUID = Field(default_factory=UUID, primary_key=True)
    title: str
    content: str
    is_published: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    authors: List["UserDB"] = Relationship(
        back_populates="courses",
        link_model=CourseUser
    )
