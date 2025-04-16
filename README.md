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
