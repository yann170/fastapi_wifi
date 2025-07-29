# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from models.auth import Token, RegisterRequest # Importez les modèles
from services import auth_service # Importez le service d'authentification
from dependencie import get_current_user # Importez la dépendance

router = APIRouter()

@router.post("/register", response_model=Token)
async def register_user_route(request: RegisterRequest):
    user = auth_service.register_user(request.username, request.password, request.email)
    if not user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    access_token = auth_service.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token_route(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_users_me_route(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user