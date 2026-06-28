from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.get("/models")
def models():

    return {
        "models": [
            "esm2_only",
            "esm2_physchem",
            "prott5_only",
            "prott5_physchem",
            "esm2_prott5",
            "esm2_prott5_physchem"
        ]
    }


@router.get("/system-info")
def system_info():

    try:
        import torch
    except ImportError:
        return {
            "device": "cpu",
            "cuda_available": False,
            "warning": "torch is not installed"
        }

    if torch.cuda.is_available():

        return {
            "device": "cuda",
            "gpu": torch.cuda.get_device_name(0),
            "cuda_available": True
        }

    return {
        "device": "cpu",
        "cuda_available": False
    }
