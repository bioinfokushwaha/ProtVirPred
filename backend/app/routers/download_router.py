from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import (
    FileResponse
)

router = APIRouter()


@router.get(
    "/download/{filename}"
)
def download_file(
    filename: str
):

    filepath = (
        Path("exports")
        / filename
    )

    if not filepath.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/csv"
    )
    
    # Model downloads
@router.get(
    "/download-model/{filename}"
)
def download_model(
    filename: str
):

    filepath = (
        Path("downloads")
        / "models"
        / filename
    )

    if not filepath.exists():

        raise HTTPException(
            status_code=404,
            detail="Model file not found"
        )

    return FileResponse(
        path=filepath,
        filename=filename
    )


# Dataset download
@router.get(
    "/download-dataset"
)
def download_dataset():

    filepath = (
        Path("downloads")
        / "datasets"
        / "benchmark_datasets.zip"
    )

    if not filepath.exists():

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return FileResponse(
        path=filepath,
        filename="benchmark_datasets.zip"
    )


# Python script download
@router.get(
    "/download-script"
)
def download_script():

    filepath = (
        Path("downloads")
        / "standalone_python_pipeline"
        / "predict_virulence.py"
    )

    if not filepath.exists():

        raise HTTPException(
            status_code=404,
            detail="Script not found"
        )

    return FileResponse(
        path=filepath,
        filename="predict_virulence.py"
    )