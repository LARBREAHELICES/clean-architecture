from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.application.controllers.auth_controller import AuthController
from app.api.deps import get_auth_controller

from app.domain.dtos.token_dto import TokenDTO
from app.domain.dtos.user_dto import UserDTO
from app.domain.dtos.login_dto import LoginDTO

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", response_model=TokenDTO)
def login(
    credential: LoginDTO,
    controller: AuthController = Depends(get_auth_controller)
):
    
    return controller.login(credential)

@router.get("/me", response_model=UserDTO)
def read_users_me(
    token: str = Depends(oauth2_scheme),
    controller: AuthController = Depends(get_auth_controller)
):
    return controller.get_current_user(token)