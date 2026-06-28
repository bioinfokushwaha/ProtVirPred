from fastapi import APIRouter

from app.services.device_service import (
    get_device
)

router = APIRouter()


@router.get("/device")
def device_info():

    return {
        "device": str(get_device())
    }
