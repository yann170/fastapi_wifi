# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated
import logging

from config import settings
from database import get_user_from_db # Importez votre fonction pour récupérer l'utilisateur

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") # Mettre le bon chemin vers votre endpoint token

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user_from_db(username) # Récupérer l'utilisateur de votre DB
        if user is None:
            raise credentials_exception
        return user
    except JWTError as e:
        logger.error(f"Erreur de décodage JWT: {e}")
        raise credentials_exception