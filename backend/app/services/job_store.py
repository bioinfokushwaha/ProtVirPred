import uuid

JOBS = {}


def create_job():

    job_id = str(
        uuid.uuid4()
    )

    JOBS[job_id] = {
        "status": "queued",
        "progress": 0,
        "result": None
    }

    return job_id


def update_job(
    job_id,
    progress=None,
    status=None,
    result=None
):

    if progress is not None:
        JOBS[job_id]["progress"] = progress

    if status is not None:
        JOBS[job_id]["status"] = status

    if result is not None:
        JOBS[job_id]["result"] = result


def get_job(
    job_id
):

    return JOBS.get(job_id)