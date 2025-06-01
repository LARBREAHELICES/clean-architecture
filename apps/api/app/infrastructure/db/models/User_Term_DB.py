import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

class User_Term_DB(SQLModel, table=True): # type: ignore[misc]
    __tablename__ = "user_term"

    user_id: Optional[str] = Field(default_factory=uuid.uuid4, foreign_key="user.id", primary_key=True) # type: ignore[misc]
    term_id: Optional[str] = Field(default_factory=uuid.uuid4, foreign_key="term.id", primary_key=True) # type: ignore[misc]
