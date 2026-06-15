from fastapi import APIRouter

from app.services.batch_embedding_service import (
    generate_esm2_embeddings_batch,
    generate_prott5_embeddings_batch
)

router = APIRouter()


@router.post("/batch-feature-test")
def batch_feature_test():

    sequences = [

        "MKTIIALSYIFCLVFADYKDDDDA",

        "MNNIRKSHPLMKLAAAAAAAKKKK",

        "MGSSHHHHHHSSGLVPRGSH"
    ]

    esm = generate_esm2_embeddings_batch(
        sequences
    )

    t5 = generate_prott5_embeddings_batch(
        sequences
    )

    return {

        "esm_shape": esm.shape,

        "prott5_shape": t5.shape
    }