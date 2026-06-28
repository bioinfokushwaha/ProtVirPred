import csv
import uuid
from pathlib import Path


EXPORT_DIR = Path("exports")

EXPORT_DIR.mkdir(
    exist_ok=True
)


def export_predictions_csv(
    results
):

    filename = (
        f"predictions_"
        f"{uuid.uuid4().hex[:8]}"
        f".csv"
    )

    filepath = (
        EXPORT_DIR / filename
    )

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(
            csvfile
        )

        writer.writerow(
            [
                "Protein_ID",
                "Prediction",
                "Probability"
            ]
        )

        for row in results:

            writer.writerow(
                [
                    row["id"],
                    row["prediction"],
                    row["probability"]
                ]
            )

    return str(filepath)