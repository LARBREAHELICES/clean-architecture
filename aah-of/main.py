from fastapi import FastAPI

from app.api.routes.user_routes import router as user_router
from app.api.routes.term_routes import router as term_router

app = FastAPI()

# Inclure les routes utilisateur

app.include_router(user_router, prefix="/api/user", tags=["users"])
app.include_router(term_router, prefix="/api/term", tags=["terms"])