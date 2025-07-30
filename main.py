# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import mikrotik
from models import auth # Importe vos modules de routes
from routers import auth
from functools import lru_cache
from config import Settings, settings # Assurez-vous d'importer la fonction get_settings

app = FastAPI(title="Portail Captif MikroTik API")


origins = [
    "http://localhost",             # Pour les tests directs de FastAPI sur la machine hôte
    "http://localhost:8500",        # Si vous testez FastAPI sur 8000
    "http://localhost:8300",
    "https://1192.168.50.252:443"
    # Si vous testez votre frontend via python -m http.server 8080
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Important pour autoriser les OPTIONS (preflight) et POST
    allow_headers=["*"], # Important pour autoriser les headers comme Content-Type, Authorization
)
# ..

app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(mikrotik.router, prefix="/mikrotik", tags=["MikroTik"])

@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur le backend FastAPI de votre portail MikroTik!"}
