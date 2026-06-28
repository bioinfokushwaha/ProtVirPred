from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import sys
import uvicorn
import argparse
from pathlib import Path

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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
FRONTEND_INDEX = FRONTEND_DIST / "index.html"
FRONTEND_ASSETS = FRONTEND_DIST / "assets"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    root_path="/ParaVirPred",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

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


def api_status():

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


@app.get("/api")
def api_home():

    return api_status()


@app.get("/")
def home():

    if FRONTEND_INDEX.exists():

        return FileResponse(FRONTEND_INDEX)

    return api_status()


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):

    requested_path = (
        FRONTEND_DIST
        / full_path
    ).resolve()

    # Check if the requested file is within FRONTEND_DIST and is a file
    try:
        if (
            FRONTEND_DIST.exists()
            and requested_path.is_file()
            and FRONTEND_DIST.resolve() in requested_path.parents or requested_path == FRONTEND_DIST.resolve()
        ):
            return FileResponse(requested_path)
    except (OSError, ValueError):
        pass

    # Fall back to serving index.html for frontend routes
    if FRONTEND_INDEX.exists():
        return FileResponse(FRONTEND_INDEX)

    return api_status()


def run(host: str = "127.0.0.1", port: int = 8001, reload: bool = False):

    uvicorn.run(
        "app.server:app",
        host=host,
        port=port,
        reload=reload
    )


app.run = run


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ParaVirPred API Server")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP address")
    parser.add_argument("--port", type=int, default=8001, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Reload backend on Python changes")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, reload=args.reload)
