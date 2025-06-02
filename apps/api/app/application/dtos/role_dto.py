from typing import List, Optional
from pydantic import BaseModel

class PermissionDTO(BaseModel):
    id: Optional[str]
    name: str

class RoleDTO(BaseModel):
    id: Optional[str]
    name: str
    permissions: Optional[List[PermissionDTO]]