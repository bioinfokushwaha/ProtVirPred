import logging
import os


LOG_DIR = "logs"

LOG_FILE = os.path.join(
    LOG_DIR,
    "predictions.log"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(message)s"
    )
)


def log_prediction(
    sequence_length,
    model_name,
    prediction,
    probability
):

    logging.info(
        f"length={sequence_length} | "
        f"model={model_name} | "
        f"prediction={prediction} | "
        f"probability={probability:.4f}"
    )