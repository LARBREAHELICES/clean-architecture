### ✅ Exercice 1 : Création d’un utilisateur (logique métier)

> Implémentez un système de création d’utilisateur avec les règles suivantes :

- Un utilisateur a un **nom** et un **âge**.
- Si son âge est **strictement supérieur à 18**, il possède **1 bitcoin**.
- Si son âge est **inférieur ou égal à 18**, il possède **0.01 bitcoin**.
- Si son âge est **strictement supérieur à 50**, il **multiplie ses bitcoins par 1.002**.

👉 **Contraintes :**
- Respectez la **séparation** entre **logique métier** et **infrastructure**.
- Ne pas utiliser d’interface formelle, mais garder une structure claire (ex: service + repository).

---

### ✅ Exercice 2 : Analyse critique

> Reprenez l’un de vos projets existants et :

- Analysez la **structure actuelle**.
- Identifiez si la **logique métier est bien séparée** de l’infrastructure (accès base de données, FastAPI, etc.).
- Si ce n’est pas le cas, proposez une refactorisation ou notez ce que vous amélioreriez.


```txt
/app
  /domain
    /models
      user.py
    /repositories
      user_repository.py
    /services
      user_service.py
    /interface
      user_service_protocol.py
  /infrastructure
    /db
      database.py
    /repositories
      user_repository_impl.py
  /application
    /controllers
      user_controller.py
```



### 🌱 `domain` — le cœur métier (pas de dépendances externes)
C’est ici que vit la **logique métier**.  

#### 📁 `models/user.py`  
Contient la classe `User`, héritée de `SQLModel`. Elle décrit les **données** de ton domaine (ex : nom, email...).

#### 📁 `repositories/user_repository.py`  
Contient une **interface abstraite** (via `Protocol`) qui décrit ce qu’un `UserRepository` doit faire (ex : `create_user`, `get_user_by_id`), **sans implémentation**.

#### 📁 `services/user_service.py`  
Contient la **logique métier**. Ce fichier utilise un `UserRepository` (via l’interface) pour appliquer des règles métier :  
> Par exemple : "Créer un utilisateur seulement s’il n’existe pas".

#### 📁 `interfaces/UserServiceProtocol.py`  
Tu y déclares les **protocols (interfaces)** métiers. Ici, le contrat que doit suivre un `UserService`.

---

### 🏗️ `infrastructure` — les détails techniques
Ici, tu lies ton code à des outils concrets (PostgreSQL, SQLModel...).

#### 📁 `db/database.py`  
Configure la base de données (moteur, session, création des tables).

#### 📁 `db/models/user_db.py`  
(Optionnel ici) Sert à faire des **DTO/ORM spécialisés** si besoin. Tu peux l’unifier avec `domain.models.user` si c’est simple.

#### 📁 `repositories/user_repository_impl.py`  
L’**implémentation concrète** de l’interface `UserRepository`, avec SQLModel.  
> Ce fichier parle **à la base** : insertions, requêtes…

---

### 🚦 `application` — gestion de l'I/O (web, CLI…)
Contient les **routes, contrôleurs**, ce qui connecte le monde extérieur à ton domaine.

#### 📁 `controllers/user_controller.py`  
Fichier FastAPI avec les **routes** (ex : `POST /users`).  
Il récupère les requêtes, utilise le `UserService`, retourne la réponse.

---

### 🌍 `interfaces` — pour regrouper les I/O (optionnel)
Tu as un dossier `interfaces/controllers`, mais ce que tu appelles `application/controllers` semble être la même chose. Tu peux fusionner ou choisir l’un.

---

### 🔌 Lien entre tout ça :

```mermaid
graph TD
    UI[FastAPI Route] --> CONTROLLER[user_controller]
    CONTROLLER --> SERVICE[UserService]
    SERVICE --> REPO[UserRepository (Protocol)]
    REPO --> IMPL[UserRepositoryImpl (SQLModel)]
    IMPL --> DB[(Database)]
```

---

### Ports et adapteurs 

Dans l'architecture **Clean Architecture**, les **adaptateurs** se trouvent généralement dans la couche **infrastructure**, car ce sont eux qui "adaptent" les appels de la logique métier aux implémentations spécifiques des technologies sous-jacentes (comme la base de données, les services externes, etc.).

Cependant, dans l'**application** (la couche **application**), il n'y a pas directement d'adaptateurs. À la place, cette couche utilise **les interfaces (ou ports)** définis dans la couche **domaine** pour communiquer avec les implémentations concrètes des **adaptateurs** qui se trouvent dans l'infrastructure.

### Résumé des couches :

1. **Domaine** : Contient les **interfaces (ports)** qui définissent les comportements attendus par la logique métier. Par exemple, `UserRepositoryProtocol` définit les méthodes que doit exposer un repository (comme `create_user`, `get_user_by_id`).
  
2. **Application** : Utilise ces interfaces (ports) pour implémenter des cas d'utilisation ou des services qui manipulent les données via ces interfaces. Par exemple, `UserService` utilise `UserRepositoryProtocol` pour créer un utilisateur, mais ne sait pas comment exactement les données sont stockées.

3. **Infrastructure** : C'est là que l'**adaptateur** (comme `UserRepositoryImpl`) est défini. Cet adaptateur implémente les interfaces définies dans le domaine et contient la logique spécifique aux bases de données (par exemple avec SQLModel) ou à d'autres services externes.

### Exemple simplifié :

- **Port (interface)** : `UserRepositoryProtocol` (dans le domaine) définit la méthode `create_user`.
  
- **Service (application)** : `UserService` (dans l'application) dépend de l'interface `UserRepositoryProtocol` et appelle `create_user`.

- **Adaptateur (infrastructure)** : `UserRepositoryImpl` (dans l'infrastructure) implémente `UserRepositoryProtocol` et fait les appels nécessaires à la base de données.

Donc, **l'adaptateur** se trouve dans **l'infrastructure**, et **l'application** interagit uniquement avec les interfaces (ports), sans connaître l'implémentation concrète.

Dans l'application, tu peux avoir des cas d'utilisation ou des services comme `UserService`, mais **l'adaptateur** reste dans la couche **infrastructure**.