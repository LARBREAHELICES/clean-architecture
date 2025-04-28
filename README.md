# 🏛 Structure générale

```
app/
├── application/
│   └── api/
├── domain/
│   ├── models/
│   ├── services/
│   └── interfaces/
├── infrastructure/
│   ├── db/  
│   └── repositories/
└── main.py
```

---

# 📂 `domain/` — **Le cœur métier**

> ❗ C'est indépendant de tout : pas de base de données, pas de FastAPI ici.

- **models/** : définitions des entités (ex: `User`, `Term`, ...).
  ```python
  # domain/models/User.py
  from dataclasses import dataclass
  from typing import Optional

  @dataclass
  class User:
      id: Optional[int] 
      username: str
      bonus: int
  ```

- **services/** : logique métier.
  ```python
  # domain/services/user_service.py
  from app.domain.interfaces.UserServiceProtocol import UserServiceProtocol
  from app.domain.models.User import User
  from app.domain.models.UserResponse import UserResponse
  from app.domain.models.Term import Term


  from typing import List

  # tu hérites de UserServiceProtocol qui est l'interface
  class UserService:
      def __init__(self, user_repository: UserServiceProtocol):
          self.user_repository = user_repository

      def create_user(self, user: User) -> User:
          return self.user_repository.create(user)

      def get_user_by_id(self, user_id: int) -> User:
          return self.user_repository.get_user_by_id(user_id)

      def list_users(self) -> list[User]:
          return self.user_repository.list_users()
      
      def sum_bonus(self, coeff : float = 1.1) -> int:
          # logique métier on augmente de 10% les bonus
          return sum( user.bonus*coeff for user in self.list_users()) 
      
      def list_terms_for_user(self, user_id: int) -> UserResponse:
          # Récupérer l'utilisateur et ses termes
          return self.user_repository.list_terms_for_user(user_id)
        
  ```

- **interfaces/** : **Protocol** (interfaces abstraites).
  ```python
  from typing import Protocol
  from app.domain.models.User import User
  from app.domain.models.UserResponse import UserResponse
  from typing import List

  """
  Comportement utiliser par le domaine => 3 méthodes à implémenter 
  Pas de dépendances avec l'infrastructure 
  """

  class UserServiceProtocol(Protocol):
      def create_user(self, user: User) -> User:
          ...
      
      def get_user_by_id(self, user_id: int) -> User | None:
          ...
      
      def list_users(self) -> List[User]:
          ...
          
      def get_user_by_id_with_terms(self) -> UserResponse:
          ...
  ```

---

# 📂 `infrastructure/` — **La partie technique**

> ❗ Cela implémente concrètement ce que le domaine demande.

- **db/** : connexion BDD, schémas SQLModel.
  ```python
  # infrastructure/db/database.py
  # app/infrastructure/db/database.py
  from sqlmodel import Session, create_engine, SQLModel
  from dotenv import load_dotenv
  import os

  # ⚡ On importe les modèles d'infrastructure !
  from app.infrastructure.db.models.UserDB import UserDB
  from app.infrastructure.db.models.TermDB import TermDB
  from app.infrastructure.db.models.User_Term_DB import User_Term_DB

  # Charger les variables d'environnement
  load_dotenv()

  # Récupérer l'URL de la base
  DATABASE_URL = os.getenv("DATABASE_URL")

  # Créer un moteur
  engine = create_engine(DATABASE_URL)

  # Session locale
  def SessionLocal() -> Session:
      return Session(bind=engine)

  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()

  # Créer les tables
  def create_db():
      SQLModel.metadata.create_all(bind=engine)
      print("Tables créées avec succès.")
  ```

---

# 📂 `application/` — **Le point d'entrée API**

> ❗ Ici, on fait le lien entre HTTP (FastAPI) et ton domaine.

- **api/** : routers FastAPI
  ```python
  # app/controllers/user_controller.py
  from app.domain.services.user_service import UserService
  from app.domain.services.term_service import TermService

  from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
  from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl

  from sqlmodel import Session
  from app.domain.models.User import User
  from app.domain.models.UserResponse import UserResponse
  from app.domain.models.Term import Term

  from app.infrastructure.db.schemas.user_schema import UserCreateRequest

  from typing import List

  class UserController:
    def __init__(self, db: Session):
        self.db = db
        
        self.user_repository = UserRepositoryImpl(db)
        self.user_service = UserService(self.user_repository)
        
        self.term_repository = TermRepositoryImpl(db)
        self.term_service = TermService(self.term_repository)
    
    def create_user(self, user: UserCreateRequest) -> User:
        
        return self.user_service.create_user(user)
    
    def get_user_by_id(self, user_id: int) -> User:
        
        return self.user_service.get_user_by_id(user_id)
    
    def list_users(self) -> List[User]:
        
        return self.user_service.list_users()
    
    def add_term_to_user(self, user_id: int, term_id: int) -> User:
        
        user = self.user_service.get_user_by_id(user_id)
        if user:
            self.term_service.add_term_to_user(user_id, term_id)
        return user

    def list_terms_for_user(self, user_id: int)-> UserResponse:
        
        return self.user_service.list_terms_for_user(user_id)
  ```

---

# 📄 `main.py` — **L'assemblage**

```python
# main.py
app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(term_router, prefix="/api")
```

---

# 🧠 Résumé 

- On respecte **l'inversion des dépendances** : le domaine ne dépend jamais de l'infrastructure ✅
- On sépare les **modèles métiers** (`domain/models`) et les **schemas API** (`infrastructure/db/schemas`) ✅
- On utilise **SQLModel** pour simplifier l'ORM ✅
- On garde ton **FastAPI** concentré uniquement sur l'API (pas de logique métier dedans) ✅

