# database.py
from passlib.context import CryptContext
from typing import Dict, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Base de données d'utilisateurs factice
fake_users_db: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": get_password_hash("secure_admin_password_123"),
        "disabled": False,
        "forfait_actif": True,
        "mikrotik_profile": "2mbps-limit",
        "mikrotik_user_prefix": "adh",
    }
}

# Fonctions pour interagir avec la DB factice (à remplacer par des requêtes DB réelles)
def get_user_from_db(username: str):
    return fake_users_db.get(username)

def add_user_to_db(user_data: Dict[str, Any]):
    fake_users_db[user_data["username"]] = user_data