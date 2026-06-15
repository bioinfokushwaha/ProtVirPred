from pathlib import Path

from app.services.fasta_parser import (
    parse_fasta
)

from app.services.batch_prediction_service import (
    predict_batch
)

from app.services.validation_service import (
    validate_sequence
)

from app.services.csv_export_service import (
    export_predictions_csv
)

from app.services.fasta_limit_service import (
    validate_fasta_sequence_count
)


def predict_fasta(
    fasta_text,
    model_name
):

    proteins = parse_fasta(
        fasta_text
    )

    validate_fasta_sequence_count(
        proteins
    )

    sequences = []

    ids = []

    for seq_id, sequence in proteins:

        sequence = validate_sequence(
            sequence
        )

        ids.append(
            seq_id
        )

        sequences.append(
            sequence
        )

    predictions = predict_batch(
        sequences,
        model_name
    )

    results = []

    for seq_id, pred in zip(
        ids,
        predictions
    ):

        results.append({
            "id": seq_id,
            "prediction": pred["prediction"],
            "probability": pred["probability"]
        })

    csv_path = export_predictions_csv(
        results
    )

    filename = Path(
        csv_path
    ).name

    return {
        "model": model_name,
        "total_sequences": len(results),
        "csv_download_url":
            f"/download/{filename}",
        "results": results
    }