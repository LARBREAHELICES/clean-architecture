from app.infrastructure.db.database import SessionLocal

def test_connection():
    try:
        db = SessionLocal()
        print("✅ Connexion à la base réussie")
    except Exception as e:
        print("❌ Erreur de connexion :", e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
