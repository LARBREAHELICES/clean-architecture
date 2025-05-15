from dataclasses import dataclass
from typing import Optional, List

class TokenBase:
    access_token: str
    token_type: str

class TokenData(TokenBase):
    username: str | None = None