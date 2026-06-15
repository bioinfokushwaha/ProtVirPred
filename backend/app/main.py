from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware

import sys

if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except:
        pass

from app.config import (
    APP_NAME,
    APP_VERSION
)

from app.services.rate_limit_service import (
    limiter
)

from app.services.model_loader import (
    load_all_models
)

from app.services.embedding_service import (
    load_embedding_models
)

from app.exception_handlers import (
    register_exception_handlers
)

from app.routers.test_router import (
    router as test_router
)

from app.routers.predict_router import (
    router as predict_router
)

from app.routers.fasta_test_router import (
    router as fasta_test_router
)

from app.routers.predict_fasta_router import (
    router as predict_fasta_router
)

from app.routers.system_router import (
    router as system_router
)

from app.routers.batch_test_router import (
    router as batch_test_router
)

from app.routers.batch_feature_router import (
    router as batch_feature_router
)

from app.routers.batch_prediction_test_router import (
    router as batch_prediction_test_router
)

from app.routers.fasta_prediction_router import (
    router as fasta_prediction_router
)

from app.routers.download_router import (
    router as download_router
)

from app.routers.device_router import (
    router as device_router
)

from app.routers.job_router import (
    router as job_router
)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

# Rate Limiter
app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# Global Exception Handlers
register_exception_handlers(
    app
)

# Routers
app.include_router(test_router)

app.include_router(predict_router)

app.include_router(fasta_test_router)

app.include_router(predict_fasta_router)

app.include_router(system_router)

app.include_router(batch_test_router)

app.include_router(batch_feature_router)

app.include_router(batch_prediction_test_router)

app.include_router(fasta_prediction_router)

app.include_router(download_router)

app.include_router(device_router)

app.include_router(job_router)

@app.on_event("startup")
def startup_event():

    print(
        f"\nStarting {APP_NAME}..."
    )

    load_all_models()

    load_embedding_models()

    print(
        "\nAPI Ready"
    )


@app.get("/")
def home():

    return {
        "status": "running",
        "api": APP_NAME,
        "version": APP_VERSION,
        "endpoints": [
            "/predict",
            "/predict-fasta",
            "/predict-fasta-file",
            "/batch-test",
            "/batch-feature-test",
            "/batch-predict-test",
            "/health",
            "/models",
            "/system-info"
        ]
    }