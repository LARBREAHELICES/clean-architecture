from fastapi import HTTPException, status
from app.domain.services.auth_service import UserAuthService
from app.application.dtos.token_dto import TokenDTO
from app.application.dtos.user_dto import UserDTO
from app.application.dtos.login_dto import LoginDTO
from app.application.mappers.user_mapper import domain_to_dto_user


class AuthController:
    def __init__(self, auth_service: UserAuthService):
        self.auth_service = auth_service

    def login(self, login_dto: LoginDTO) -> TokenDTO:
        user = self.auth_service.authenticate(login_dto.username, login_dto.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = self.auth_service.security.create_access_token(data={"sub": user.username})
        return TokenDTO(access_token=token, token_type="bearer")

    def get_current_user(self, token: str) -> UserDTO:
        user = self.auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return domain_to_dto_user(user)
