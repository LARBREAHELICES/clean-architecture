from fastapi import FastAPI
from app.application.controllers.user_controller import router as user_router

app = FastAPI()

# Inclure les routes utilisateur
app.include_router(user_router, prefix="/api")