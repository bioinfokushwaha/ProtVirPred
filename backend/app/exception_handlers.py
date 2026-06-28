from fastapi import (
    FastAPI,
    Request
)

from fastapi.responses import (
    JSONResponse
)

from fastapi.exceptions import (
    HTTPException
)


def register_exception_handlers(
    app: FastAPI
):

    @app.exception_handler(
        HTTPException
    )
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail
            }
        )

    @app.exception_handler(
        Exception
    )
    async def generic_exception_handler(
        request: Request,
        exc: Exception
    ):

        return JSONResponse(
            status_code=500,
            content={
                "error": str(exc)
            }
        )