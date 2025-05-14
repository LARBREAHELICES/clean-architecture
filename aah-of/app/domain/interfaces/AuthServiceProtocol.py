# app/domain/interfaces/AuthServiceProtocol.py
from typing import Protocol


class AuthServiceProtocol(Protocol):
    def authenticate(self) -> None:
        ...

    def hash_pass(password:str)->str:
        ...