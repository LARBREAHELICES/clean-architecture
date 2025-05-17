from fastapi import HTTPException, status
from app.domain.services.auth_service import UserAuthService

from app.application.dtos.token_dto import TokenDTO
from app.application.dtos.user_dto import UserDTO
from app.application.dtos.login_dto import LoginDTO

class AuthController:
    def __init__(self, auth_service: UserAuthService):
        self.auth_service = auth_service

    def login(self, login_dto: LoginDTO) -> TokenDTO:
        user = self.auth_service.authenticate(login_dto.username, login_dto.password)
        if not user:
            raise ValueError("Invalid credentials")
        
        token = self.auth_service.security.create_access_token(data={"sub": user.username})
        
        return TokenDTO(access_token=token, token_type="bearer")

    def get_current_user(self, token: str) -> UserDTO:
        user = self.auth_service.get_user_from_token(token)
        
        return UserDTO(**user.model_dump())  # ou `.dict()` selon ton modèle
