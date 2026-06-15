from fastapi import APIRouter

from app.services.batch_feature_builder import (
    build_batch_features
)

router = APIRouter()


@router.post("/batch-feature-test")
def batch_feature_test():

    sequences = [
        "MKTIIALSYIFCLVFADYKDDDDK",
        "MNNNKLAVVVAAALAAPAAA",
        "MKVLWAALLVTFLAGCQAKVE"
    ]

    features = build_batch_features(
        sequences,
        "esm2_prott5_physchem"
    )

    return {
        "shape": features.shape
    }