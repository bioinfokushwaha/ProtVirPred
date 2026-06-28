from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Logs
LOG_DIR = BASE_DIR / "logs"
PREDICTION_LOG_FILE = LOG_DIR / "predictions.log"

# Prediction threshold
PREDICTION_THRESHOLD = 0.5

# Prediction Batch Size
PREDICTION_BATCH_SIZE = 100

# Validation
MIN_SEQUENCE_LENGTH = 20
MAX_SEQUENCE_LENGTH = 10000

# FASTA upload limits
MAX_FASTA_SEQUENCES = 1000
MAX_FASTA_FILE_SIZE_MB = 10

# Embedding dimensions
ESM2_DIM = 1280
PROTT5_DIM = 1024

# API
APP_NAME = "ParaVirPred"
APP_VERSION = "1.0.0"