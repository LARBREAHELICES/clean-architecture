
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class BaseUser:
    username: str
    bonus: int
    email: str
    is_active: bool

@dataclass
class User(BaseUser):
    id: Optional[str] 

@dataclass
class UserCreate(BaseUser):
    pass
    
@dataclass
class UserWithPassword(BaseUser):
    password: str
    
@dataclass
class UserwithoutPassword(BaseUser):
    pass

@dataclass
class UserTerms(BaseUser):
    id: Optional[str] 
    terms: List["Term"]
    
    
    """
    from dataclasses import dataclass, field
from typing import Optional, List

# --- Permissions définies sous forme de str pour simplicité (on pourrait aussi faire une Enum) ---
@dataclass
class Permission:
    name: str  # ex : "view_trainer_availability"

# --- Rôle avec liste de permissions ---
@dataclass
class Role:
    name: str  # ex : "admin", "trainer", "manager"
    permissions: List[Permission] = field(default_factory=list)

# --- Base utilisateur ---
@dataclass
class BaseUser:
    username: str
    bonus: int
    email: str
    is_active: bool
   # role: Role  # Ajout du rôle ici

# --- Utilisateur complet ---
@dataclass
class User(BaseUser):
    id: Optional[str]

# --- Utilisateur à la création (sans id) ---
@dataclass
class UserCreate(BaseUser):
    password: str  # Ajouté ici pour création

# --- Utilisateur avec password (utile pour authentification) ---
@dataclass
class UserWithPassword(BaseUser):
    password: str

# --- Utilisateur sans password (pour réponse API, par ex) ---
@dataclass
class UserWithoutPassword(BaseUser):
    pass

# --- Utilisateur avec termes associés (ex : disponibilité, affectations, etc.) ---
@dataclass
class UserTerms(BaseUser):
    id: Optional[str]
    terms: List["Term"]

    
    """