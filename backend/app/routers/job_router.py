from fastapi import APIRouter

from app.services.job_store import (
    get_job
)

router = APIRouter()


@router.get(
    "/job/{job_id}"
)
def job_status(
    job_id: str
):

    job = get_job(
        job_id
    )

    if not job:

        return {
            "error": "Job not found"
        }

    return job