import numpy as np
import torch

from app.services.feature_builder import (
    build_features
)
from app.services.model_loader import (
    get_model
)
from app.services.prediction_logger import (
    log_prediction
)
from app.config import (
    PREDICTION_THRESHOLD
)
from app.services.device_service import (
    DEVICE
)

def predict_sequence(
    sequence,
    combination
):
    feature_vector = build_features(
        sequence,
        combination
    )
    model_info = get_model(
        combination
    )
    model = model_info["model"]

    scaler = model_info.get(
        "scaler"
    )
    X = feature_vector.reshape(
        1,
        -1
    )
    if model_info["type"] == "dnn":
        model = model.to(DEVICE)
        model.eval()

        X = scaler.transform(X)
        X_tensor = torch.FloatTensor(
            X
        ).to(DEVICE)
        with torch.no_grad():

            prob = model(
                X_tensor
            ).item()
    elif model_info["type"] == "xgb":

        if scaler is not None:

            X = scaler.transform(X)

        prob = model.predict_proba(
            X
        )[0, 1]

    elif model_info["type"] == "svm":

        if scaler is not None:

            X = scaler.transform(
                X
            )
        if hasattr(
            model,
            "predict_proba"
        ):
            prob = model.predict_proba(
                X
            )[0, 1]
        else:
            decision = (
                model.decision_function(
                    X
                )[0]
            )

            prob = 1 / (
                1 + np.exp(
                    -decision
                )
            )
    else:
        raise ValueError(
            "Unsupported model type"
        )
    prediction = (
        "Virulent"
        if prob >= PREDICTION_THRESHOLD
        else "Non-Virulent"
    )
    probability = round(
        float(prob),
        4
    )
    log_prediction(
        sequence_length=len(sequence),
        model_name=combination,
        prediction=prediction,
        probability=probability
    )
    return {
        "prediction": prediction,
        "probability": probability
    }