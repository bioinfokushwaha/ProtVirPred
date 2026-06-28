from fastapi import (
    APIRouter,
    Request
)

from app.schemas.prediction import (
    PredictionRequest
)

from app.services.prediction_service import (
    predict_sequence
)

from app.services.validation_service import (
    validate_sequence
)

from app.services.rate_limit_service import (
    limiter
)

router = APIRouter()


@router.post("/predict")
@limiter.limit("20/minute")
def predict(
    request: Request,
    data: PredictionRequest
):

    sequence = validate_sequence(
        data.sequence
    )

    result = predict_sequence(
        sequence,
        data.combination
    )

    return result