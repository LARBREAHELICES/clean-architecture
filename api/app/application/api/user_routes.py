# app/api/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.application.controllers.user_controller import UserController
from app.infrastructure.db.schemas.user_schema import UserCreateRequest
from app.domain.models.User import User
from app.domain.models.UserResponse import UserResponse
from typing import List

from app.infrastructure.db.database import get_db
from sqlmodel import Session

router = APIRouter()

# Dépendance pour obtenir le contrôleur
def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

# Créer un utilisateur
@router.post("/create", response_model=User)
async def create_user(user: UserCreateRequest, user_controller: UserController = Depends(get_user_controller)):
    
    return user_controller.create_user(user)

# Lister tous les utilisateurs
@router.get("/all", response_model=List[User])
def list_users(user_controller: UserController = Depends(get_user_controller)):
    
    return user_controller.list_users()

# Obtenir un utilisateur par ID
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, user_controller: UserController = Depends(get_user_controller)):
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/terms", response_model=UserResponse)
def get_user(user_id: int, user_controller: UserController = Depends(get_user_controller)):
    user = user_controller.list_terms_for_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Ajouter un term à un utilisateur existant
@router.post("/{user_id}/add_term/{term_id}", response_model=User)
def add_term_to_user(user_id: int, term_id: int, user_controller: UserController = Depends(get_user_controller)):
    user = user_controller.add_term_to_user(user_id, term_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
