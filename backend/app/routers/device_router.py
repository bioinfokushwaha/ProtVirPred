from fastapi import APIRouter

from app.services.device_service import (
    DEVICE
)

router = APIRouter()


@router.get("/device")
def device_info():

    return {
        "device": str(DEVICE)
    }