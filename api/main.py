# app/main.py

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from sqlmodel import SQLModel

from app.infrastructure.db import SessionDep, engine
from app.infrastructure.user_repository import UserRepository
from app.domain.user_service import UserService
from app.domain.models import User  # ton modèle SQLModel

# Création des tables au démarrage
SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic models pour les I/O
class UserIn(BaseModel):
    username: str
    age: int

class UserOut(BaseModel):
    username: str
    age: int
    bonus: int

# Dépendance FastAPI pour obtenir le service
def get_user_service():
    db = SessionDep()
    try:
        repo = UserRepository(db)
        
        return UserService(repo)
    finally:
        db.close()


@app.get("/", tags=["Root"])
def home():
    return {"message": "Hello from FastAPI with Docker, PostgreSQL, and Adminer!"}

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn, service: UserService = Depends(get_user_service)):
    
    return service.create_user(user.username, user.age)

@app.get("/users", response_model=List[UserOut])
def list_users(service: UserService = Depends(get_user_service)):
    
    return service.get_all_users()
