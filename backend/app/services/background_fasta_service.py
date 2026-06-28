from pathlib import Path

from app.services.job_store import (
    update_job
)

from app.services.fasta_parser import (
    parse_fasta
)

from app.services.validation_service import (
    validate_sequence
)

from app.services.batch_prediction_service import (
    predict_batch
)

from app.services.csv_export_service import (
    export_predictions_csv
)


def process_fasta_job(
    job_id,
    fasta_text,
    model_name
):

    update_job(
        job_id,
        status="running",
        progress=5
    )

    proteins = parse_fasta(
        fasta_text
    )

    sequences = []
    ids = []

    total = len(proteins)

    for i, (seq_id, seq) in enumerate(proteins):

        seq = validate_sequence(
            seq
        )

        ids.append(seq_id)

        sequences.append(seq)

        update_job(
            job_id,
            progress=int(
                (i / total) * 30
            )
        )

    predictions = predict_batch(
        sequences,
        model_name
    )

    update_job(
        job_id,
        progress=80
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

    update_job(
        job_id,
        status="completed",
        progress=100,
        result={
            "csv_download_url":
                f"/download/{filename}",
            "results": results
        }
    )