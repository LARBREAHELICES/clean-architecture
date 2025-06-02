from typing import List
from app.domain.models.User import Role, Permission
from app.infrastructure.db.models.RoleDB import RoleDB
from app.application.dtos.role_dto import RoleDTO, PermissionDTO

def orm_to_domain_role(role_db: RoleDB) -> Role:
    return Role(
        id=role_db.id,
        name=role_db.name,
        permissions=[
            Permission(id=p.id, name=p.name) for p in role_db.permissions
        ] if role_db.permissions else []
    )
    

def domain_to_dto_role(role: Role) -> RoleDTO:
    return RoleDTO(
        id=role.id,
        name=role.name,
        permissions=[
            PermissionDTO(id=perm.id, name=perm.name) for perm in role.permissions or []
        ]
    )