from fastapi import APIRouter

from app.services.fasta_parser import (
    parse_fasta
)

router = APIRouter()


@router.post("/test-fasta")
def test_fasta(data: dict):

    fasta = data["fasta"]

    sequences = parse_fasta(fasta)

    return {
        "count": len(sequences),
        "sequences": sequences
    }