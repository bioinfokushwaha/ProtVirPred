from fastapi import APIRouter

from app.services.embedding_service import (
    generate_esm2_embedding
)

from app.services.embedding_service import (
    generate_prott5_embedding
)
router = APIRouter()


@router.get("/test-esm")

def test_esm():

    seq = (
        "MKTIIALSYIFCLVFADYKDDD"
    )

    emb = generate_esm2_embedding(
        seq
    )

    return {
        "shape": list(
            emb.shape
        )
    }

@router.get("/test-prott5")
def test_prott5():

    seq = (
        "MKTIIALSYIFCLVFADYKDDD"
    )

    emb = generate_prott5_embedding(
        seq
    )

    return {
        "shape": list(
            emb.shape
        )
    }