# app/api/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.application.controllers.user_controller import UserController
from app.api.schemas.user_schema import UserCreateRequest
from app.api.schemas.user_schema import UserResponse, UserTermResponse
from typing import List, Annotated

from app.infrastructure.db.database import get_db
from sqlmodel import Session

router = APIRouter()

# Dépendance pour obtenir le contrôleur
def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)

# Créer un utilisateur
@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreateRequest, user_controller: UserController = Depends(get_user_controller)):
    return user_controller.create_user(user)

# Lister tous les utilisateurs
@router.get("/all", response_model=List[UserResponse])
def list_users(user_controller: UserController = Depends(get_user_controller)):
    
    return user_controller.list_users()

# Obtenir un utilisateur par ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user_controller: UserController = Depends(get_user_controller)):
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/terms", response_model=UserTermResponse)
def get_user_with_terms(user_id: int, user_controller: UserController = Depends(get_user_controller)):
    
    return user_controller.get_user_with_terms(user_id)

@router.post("/{user_id}/assign-terms", response_model=UserTermResponse)
async def assign_terms(
    user_id: int,
    term_ids: List[int],
    controller: UserController = Depends(get_user_controller)
):
    return controller.assign_terms_to_user(user_id, term_ids)

@router.get("/term/{term_id}/users", response_model=List[UserResponse])
def get_users_for_term(
    term_id: int,
    controller: UserController = Depends(get_user_controller)
):
    return controller.get_users_by_term(term_id)