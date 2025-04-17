from app.domain.models import User
from app.infrastructure.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo # c'est genre une interface documentée


    def create_user(self, username: str, age: int) -> User:
        # logique métier 
        if age > 18:
            bonus = 1
            if age > 50:
                bonus *= 1.002
                print(bonus)
        else:
            bonus = 0.01
            print(bonus)

        return self.user_repo.create(User(username=username, age=age, bonus=bonus))

    def get_all_users(self):
        
        return self.user_repo.list_users()