# app/interfaces/controllers/router.py

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from app.application.controllers.auth_controller import AuthController
from app.application.dtos.login_dto import LoginDTO
from app.application.dtos.user_dto import UserDTO
from app.domain.services.auth_service import UserAuthService

router = APIRouter()

from app.api.deps import get_auth_controller

@router.post("/login", response_class=JSONResponse)
def login(
    login_dto: LoginDTO,
    controller: AuthController = Depends(get_auth_controller)
):
    return controller.login(login_dto)

@router.post("/refresh", response_class=JSONResponse)
def refresh(
    request: Request,
    controller: AuthController = Depends(get_auth_controller)
):
    return controller.refresh(request)

@router.post("/logout", response_class=JSONResponse)
def logout(
    controller: AuthController = Depends(get_auth_controller)
):
    return controller.logout()

@router.get("/me", response_model=UserDTO)
def me(
    request: Request,
    controller: AuthController = Depends(get_auth_controller)
):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token_value = token.split(" ")[1]
    
    return controller.get_current_user(token_value)
