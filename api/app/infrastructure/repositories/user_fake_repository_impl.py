from typing import List
from app.domain.models.user import User
from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol 
from app.domain.models.user import User

users = [
    {"id": 1, "username": "john_doe", "bonus": 50, "category": "developer", "note": 5},
    {"id": 2, "username": "jane_smith", "bonus": 75,  "category": "integrateur ux", "note": 4},
    {"id": 3, "username": "alice_wonder", "bonus": 20,  "category": "developer", "note": 4},
    {"id": 4, "username": "bob_marley", "bonus": 90,  "category": "developer", "note": 2},
    {"id": 5, "username": "charlie_brown", "bonus": 60,  "category": "ui designer", "note": 3},
    {"id": 6, "username": "david_lee", "bonus": 85,  "category": "developer", "note": 4},
    {"id": 7, "username": "emma_rock", "bonus": 40,  "category": "developer", "note": 5},
    {"id": 8, "username": "frankie_doe", "bonus": 100,  "category": "ui designer", "note": 4},
    {"id": 9, "username": "grace_hopper", "bonus": 30,  "category": "developer", "note": 3},
    {"id": 10, "username": "henry_ford", "bonus": 65,  "category": "product owner", "note": 4},
]

"""
L'infrastructure implémente l'interface et fait concrètement les requêtes
"""
class UserFakeRepositoryImpl(UserServiceProtocol):

    def create(self, user: User) -> User:
        users.append(user)
        
        return User(username=user.username, bonus=user.bonus)

    def list_users(self) -> List[User]:

        return [User(username=user['username'], bonus=user['bonus'], category=user['category']) for user in users]
    
    def get_user_by_id(self, user_id: int) -> User| None:
        userList = list(filter(lambda user: user["id"] == user_id, users))
        
        return  User(**userList[0]) if len(userList) > 0 else None
    
    def get_users_by_category(self, category: str) -> List[User]:
        return [User(username=user['username'], bonus=user['bonus'], category=user['category'], note=user['note']) for user in users if user['category'] == category]

    