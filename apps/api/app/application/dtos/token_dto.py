from dataclasses import dataclass

from pydantic import BaseModel

class TokenDTO(BaseModel):
    access_token: str
    token_type: str

class TokenDTOData(BaseModel):
    username: str | None = None