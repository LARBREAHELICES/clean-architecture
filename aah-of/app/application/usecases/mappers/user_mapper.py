
from app.api.schemas.user_schema import UserCreateRequest, UserResponse
from app.domain.models.User import User

from typing import List

class UserMapper:
    @staticmethod
    def from_request(user_req: UserCreateRequest) -> User:
        return User(id=None, username=user_req.username, bonus=user_req.bonus)

    @staticmethod
    def to_response(user: User) -> UserResponse:
        return UserResponse(id=user.id, username=user.username, bonus=user.bonus)
    
    @staticmethod
    def to_responses(users: List[User]) -> List[UserResponse]:
        
        return [UserResponse(id=user.id, username=user.username, bonus=user.bonus) for user in users]
    