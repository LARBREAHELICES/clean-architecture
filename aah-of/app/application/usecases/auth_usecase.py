# app/application/usecases/auth_usecase.py
from app.domain.interfaces.AuthServiceProtocol import AuthServiceProtocol

class AuthUseCase:
    def __init__(self, service: AuthServiceProtocol):
        self.service = service