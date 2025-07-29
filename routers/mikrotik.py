# routers/mikrotik.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from concurrent.futures import ThreadPoolExecutor
import logging

from dependencie import get_current_user
from services import mikrotik_service
from models.mikrotik import MikrotikVoucherResponse

logger = logging.getLogger(__name__)

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=5) # Pour les opérations bloquantes MikroTik

@router.post("/generate-mikrotik-voucher", response_model=MikrotikVoucherResponse)
async def generate_mikrotik_voucher_route(current_user: Annotated[dict, Depends(get_current_user)]):
    """
    Génère ou met à jour un utilisateur Hotspot MikroTik pour l'utilisateur authentifié.
    """
    if not current_user["forfait_actif"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Votre compte n'a pas de forfait actif pour générer un voucher."
        )

    app_username = current_user["username"]
    mikrotik_profile = current_user["mikrotik_profile"]
    mikrotik_user_prefix = current_user["mikrotik_user_prefix"]

    mikrotik_username, mikrotik_password = mikrotik_service.generate_mikrotik_voucher_details(mikrotik_user_prefix)

    try:
        # Exécuter l'opération MikroTik dans un thread séparé
        await  mikrotik_service.create_mikrotik_hotspot_user(
            mikrotik_username,
            mikrotik_password,
            mikrotik_profile
        )
        # En production, vous voudriez stocker ce voucher dans votre DB et l'associer à l'utilisateur
        return {
            "message": "Voucher MikroTik créé/mis à jour avec succès.",
            "mikrotik_username": mikrotik_username,
            "mikrotik_password": mikrotik_password,
            "mikrotik_profile": mikrotik_profile
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erreur lors de la génération du voucher pour {app_username}: {e}")
        raise HTTPException(status_code=500, detail=f"Échec de la génération du voucher: {e}")