from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Request,
    BackgroundTasks
)

from app.services.fasta_prediction_service import (
    predict_fasta
)

from app.services.fasta_limit_service import (
    validate_fasta_file_size
)

from app.services.rate_limit_service import (
    limiter
)

from app.services.job_store import (
    create_job
)

from app.services.background_fasta_service import (
    process_fasta_job
)

router = APIRouter()


@router.post("/predict-fasta-file")
@limiter.limit("5/minute")
async def predict_fasta_file(
    request: Request,
    file: UploadFile = File(...),
    model_name: str = Form(...)
):

    content = await file.read()

    validate_fasta_file_size(
        len(content)
    )

    fasta_text = content.decode()

    return predict_fasta(
        fasta_text,
        model_name
    )


@router.post("/predict-fasta-async")
@limiter.limit("5/minute")
async def predict_fasta_async(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model_name: str = Form(...)
):

    content = await file.read()

    validate_fasta_file_size(
        len(content)
    )

    fasta_text = content.decode()

    job_id = create_job()

    background_tasks.add_task(
        process_fasta_job,
        job_id,
        fasta_text,
        model_name
    )

    return {
        "job_id": job_id,
        "status": "queued"
    }