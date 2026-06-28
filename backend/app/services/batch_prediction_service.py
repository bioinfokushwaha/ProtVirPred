import gc
import torch
import numpy as np

from app.services.model_loader import (
    get_model
)
from app.services.batch_feature_builder import (
    build_batch_features
)
from app.services.device_service import (
    DEVICE
)

def clear_gpu_memory():

    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    gc.collect()

def predict_batch(
    sequences,
    model_name
):
    model_info = get_model(
        model_name
    )

    model = model_info["model"]
    scaler = model_info["scaler"]
    model_type = model_info["type"]
    features = build_batch_features(
        sequences,
        model_name
    )

    if scaler is not None:

        features = scaler.transform(
            features
        )

    results = []

    if model_type == "dnn":
        model.to(
            DEVICE
        )

        with torch.no_grad():

            x = torch.tensor(
                features,
                dtype=torch.float32,
                device=DEVICE
            )

            probs = (
                model(x)
                .detach()
                .cpu()
                .numpy()
            )

        del x
        model.to(
            "cpu"
        )

        clear_gpu_memory()

        for prob in probs:
            p = float(
                prob[0]
            )

            results.append(
                {
                    "prediction":
                        "Virulent"
                        if p >= 0.5
                        else "Non-Virulent",

                    "probability":
                        round(
                            p,
                            4
                        )
                }
            )

    else:

        probs = model.predict_proba(
            features
        )[:, 1]

        for p in probs:

            results.append(
                {
                    "prediction":
                        "Virulent"
                        if p >= 0.5
                        else "Non-Virulent",

                    "probability":
                        round(
                            float(p),
                            4
                        )
                }
            )

    del features

    gc.collect()

    return results