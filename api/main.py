# app/main.py

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
from sqlmodel import SQLModel

from app.infrastructure.db import SessionDep, engine
from app.infrastructure.user_repository import UserRepository
from DATA.FastAPI.api.app.domain.services.user_service import UserService
from DATA.FastAPI.api.app.domain.models.User import User


# Création des tables au démarrage de l'app
SQLModel.metadata.create_all(bind=engine)

app = FastAPI()


# ----- Pydantic models pour I/O ----- #

class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    username: str
    age: int
    bonus: int


# ----- Dépendances ----- #

def get_user_service(session: SessionDep ) -> UserService:
    """
    Injecte un UserService avec une session liée au moteur de base de données.
    """
    repo = UserRepository(session)
    return UserService(repo)


# ----- Endpoints ----- #

@app.get("/", tags=["Root"])
def home():
    """Point d'entrée de l'API"""
    return {"message": "Hello from FastAPI with Docker, PostgreSQL, and Adminer!"}


@app.post("/users", response_model=UserOut)
def create_user(user: UserIn, service: UserService = Depends(get_user_service)):
    """
    Crée un nouvel utilisateur.
    """
    return service.create_user(user.username, user.age)


@app.get("/users", response_model=List[UserOut])
def list_users(service: UserService = Depends(get_user_service)):
    """
    Liste tous les utilisateurs.
    """
    return service.get_all_users()
