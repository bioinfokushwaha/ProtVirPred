from fastapi import APIRouter

from app.services.batch_physchem_service import (
    calculate_physchem_batch
)

router = APIRouter()


@router.post("/batch-physchem-test")
def batch_physchem_test():

    sequences = [
        "MKTIIALSYIFCLVFADYKDDDDK",
        "MNNNKLAVVVAAALAAPAAA",
        "MKVLWAALLVTFLAGCQAKVE"
    ]

    features = calculate_physchem_batch(
        sequences
    )

    return {
        "shape": features.shape
    }