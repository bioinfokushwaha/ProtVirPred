from fastapi import HTTPException


def raise_validation_error(
    message: str
):

    raise HTTPException(
        status_code=400,
        detail=message
    )