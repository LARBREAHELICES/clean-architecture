# 🏛 Structure générale

```
app/
├── api/
│   ├── deps.py   <-- connexion à la base de données
│   ├── routes/   <-- la couche avec l'extérieur 
├── application/
│   ├── controllers/
│   ├── usecases/
│   │   └── assign_terms_to_user.py
├── domain/
│   ├── models/
│   ├── services/
│   ├── dtos/
│   └── interfaces/
├── infrastructure/
│   ├── db/
│   │   ├── models/
│   │   └── database.py
│   └── repositories/
└── main.py
```

---


**Mappers dans une architecture hexagonale / clean architecture** :

---

### 🧭 **Côté extérieur (API / Application)**

👉 **Conversion entre :**
**`Pydantic`** (requêtes/réponses API) ⇄ **`Domain models`**
✅ Sert à *adapter les données entrantes/sortantes à ton cœur métier*

---

### 🏗️ **Côté intérieur (Infrastructure)**

👉 **Conversion entre :**
**`Domain models`** ⇄ **`SQLModel` (ou autre ORM)**
✅ Sert à *mapper entre la logique métier et la persistance réelle*

---

### Schéma simplifié (sens des échanges) :

```
Client ⇄ Pydantic ⇄ Domain ⇄ SQLModel (DB)
           ↑            ↑
        Mapper API   Mapper Infra
```

---

## Migrations

```bash
# Revenir à l'état initial
alembic downgrade base

# création d'une nouvelle migration 
alembic revision -m "add user_term associations"

# lancer les migrations
alembic upgrade head
```


```txt
Client HTTP (Frontend)
        ↓
    FastAPI Routes (api/)
        ↓
   Controller (controller/)
        ↓
     UseCase (application/)
        ↓
  Domain Service / Model (domain/)
        ↓
Infrastructure (repository, DB, etc.)
```