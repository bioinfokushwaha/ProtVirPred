from fastapi import APIRouter

from app.services.batch_prediction_service import (
    predict_batch
)

router = APIRouter()


@router.post("/batch-predict-test")
def batch_predict_test():

    sequences = [
        "MKTIIALSYIFCLVFADYKDDDDK",
        "MNNNKLAVVVAAALAAPAAA",
        "MKVLWAALLVTFLAGCQAKVE"
    ]

    results = predict_batch(
        sequences,
        "esm2_prott5_physchem"
    )

    return {
        "results": results
    }