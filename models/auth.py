from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    # hashed_password n'est pas inclus ici car c'est une information sensible
    # et nous n'avons pas besoin de la sérialiser pour les réponses directes

class UserInDB(User):
    hashed_password: str
    forfait_actif: bool
    mikrotik_profile: str
    mikrotik_user_prefix: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None