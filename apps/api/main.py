from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5175",  # adresse locale React
    "http://127.0.0.1:5175",  # parfois React utilise cette IP locale
]

from app.api.routes.user_routes import router as user_router
from app.api.routes.term_routes import router as term_router
from app.api.routes.auth_routes import router as auth_router

from app.api.routes.reporting_summary_routes import router as reporting_summary_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # liste des domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],  # autorise tous les types de méthodes (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],  # autorise tous les headers
)

# Inclure les routes utilisateur

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

app.include_router(user_router, prefix="/api/user", tags=["users"])
app.include_router(term_router, prefix="/api/term", tags=["terms"])

app.include_router(reporting_summary_router, prefix="/api/reporting-summary", tags=["reportingSummary"])   