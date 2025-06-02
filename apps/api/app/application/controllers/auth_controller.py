from fastapi import Response, Request, HTTPException, status
from fastapi.responses import JSONResponse

from app.domain.services.auth_service import UserAuthService
from app.application.dtos.login_dto import LoginDTO
from app.application.dtos.user_dto import UserDTO
from app.application.dtos.role_dto import RoleDTO, PermissionDTO

class AuthController:
    def __init__(self, auth_service: UserAuthService):
        self.auth_service = auth_service

    def login(self, login_dto: LoginDTO) -> JSONResponse:
        user = self.auth_service.authenticate(login_dto.username, login_dto.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.auth_service.security.create_access_token(user.username)
        refresh_token = self.auth_service.security.create_refresh_token(user.username)

        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.username,
            "role" : {  # Ajouter les informations de rôle
                "name": user.role.name if user.role else None,
                "permissions": [
                    { "name": p.name} for p in user.role.permissions
                ] if user.role and user.role.permissions else []
            }
        }

        response = JSONResponse(content=response_data)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,       # à adapter selon environnement (True en prod)
            samesite="strict",
            max_age=7*24*3600,  # 7 jours
            path="/"  # cookie accessible uniquement sur ce endpoint
        )

        return response

    def refresh(self, request: Request) -> JSONResponse:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing"
            )
        try:
            payload = self.auth_service.security.decode_token(refresh_token)
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user = self.auth_service.get_user_from_token(refresh_token)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            access_token = self.auth_service.security.create_access_token(user.username)

            response_data = {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user.username
            }
            return JSONResponse(content=response_data)

        except Exception:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    def logout(self) -> JSONResponse:
        response = JSONResponse(content={"detail": "Logged out"})
        response.delete_cookie("refresh_token", path="/")
        return response


    def get_current_user(self, token: str) -> UserDTO:
        user = self.auth_service.get_user_from_token(token)
        
        print(user)
        
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            bonus=user.bonus,
            role=RoleDTO(
                id=user.role.id if user.role else None,
                name=user.role.name if user.role else None,
                permissions=[PermissionDTO(id=p.id, name=p.name) for p in user.role.permissions] if user.role and user.role.permissions else []
            )
        )