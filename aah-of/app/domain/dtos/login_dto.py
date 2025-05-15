# app/domain/dtos/login_dto.py
from pydantic import BaseModel

class LoginDTO(BaseModel):
    username: str
    password: str