# services/auth_service.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Dict, Any

from config import settings
from database import get_user_from_db, add_user_to_db # Importez vos fonctions DB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str):
    user = get_user_from_db(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def register_user(username: str, password: str, email: str | None = None):
    if get_user_from_db(username):
        return False # Utilisateur déjà existant

    hashed_password = get_password_hash(password)
    new_user_data = {
        "username": username,
        "email": email,
        "full_name": username,
        "hashed_password": hashed_password,
        "disabled": False,
        "forfait_actif": False,
        "mikrotik_profile": "default",
        "mikrotik_user_prefix": "reg",
    }
    add_user_to_db(new_user_data)
    return new_user_data