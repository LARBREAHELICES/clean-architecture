from app.domain.interfaces.AuthServiceProtocol import AuthServiceProtocol

class AuthService:
    def __init__(self, auth_repository: AuthServiceProtocol):
        self.auth_repository = auth_repository
        