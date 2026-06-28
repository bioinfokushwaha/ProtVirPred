from fastapi import APIRouter

from app.services.batch_embedding_service import (
    generate_esm2_embeddings_batch
)

router = APIRouter()


@router.post("/batch-test")
def batch_test():

    sequences = [

        "MKTIIALSYIFCLVFADYKDDDDA",

        "MNNIRKSHPLMKLAAAAAAAKKKK",

        "MGSSHHHHHHSSGLVPRGSH"
    ]

    embeddings = (
        generate_esm2_embeddings_batch(
            sequences
        )
    )

    return {
        "shape": embeddings.shape
    }