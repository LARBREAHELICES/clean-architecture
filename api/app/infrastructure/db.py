from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated, Optional

from app.domain.models import User # logique métier 

# user_1 = User(username="Deadpond", age=45, bonus=0)
# user_2 = User(username="Alice", age=45, bonus = 1)
# user_3 = User(username="Bernard", age=45, bonus =0)

engine = create_engine("postgresql://sofiene:@127.0.0.1:5432/clean_archi")

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
