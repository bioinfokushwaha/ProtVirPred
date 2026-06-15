from fastapi import APIRouter

from app.services.fasta_parser import (
    parse_fasta
)

from app.services.prediction_service import (
    predict_sequence
)

from app.services.validation_service import (
    validate_sequence
)

router = APIRouter()


@router.post("/predict-fasta")
def predict_fasta(data: dict):

    fasta_text = data["fasta"]

    combination = data["combination"]

    sequences = parse_fasta(
        fasta_text
    )

    results = []

    for seq_id, sequence in sequences:

        sequence = validate_sequence(
            sequence
        )

        prediction = predict_sequence(
            sequence,
            combination
        )

        results.append(
            {
                "sequence_id": seq_id,
                **prediction
            }
        )

    return {
        "total_sequences": len(results),
        "results": results
    }