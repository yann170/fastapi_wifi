# models/mikrotik.py
from pydantic import BaseModel

class MikrotikVoucherResponse(BaseModel):
    message: str
    mikrotik_username: str
    mikrotik_password: str
    mikrotik_profile: str