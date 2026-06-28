import joblib
import torch

from app.models.deepdnn import VirulenceDNN
from app.services.model_registry import MODEL_CONFIGS
from app.services.device_service import DEVICE

LOADED_MODELS = {}

def load_all_models():
    global LOADED_MODELS

    for name, cfg in MODEL_CONFIGS.items():

        print(f"\nLoading {name}")

        if cfg["type"] == "dnn":

            checkpoint = torch.load(
                cfg["path"],
                map_location=DEVICE,
                weights_only=False
            )

            model = VirulenceDNN(
                cfg["input_dim"]
            )

            model.load_state_dict(
                checkpoint["model"]
            )
            model.to(DEVICE)

            model.eval()

            scaler = checkpoint["scaler"]

            LOADED_MODELS[name] = {
                "model": model,
                "scaler": scaler,
                "type": "dnn"
            }

        elif cfg["type"] in ["xgb", "svm"]:

            loaded = joblib.load(
                cfg["path"]
            )

            if isinstance(loaded, tuple):

                model = loaded[0]
                scaler = loaded[1]

            else:

                model = loaded
                scaler = None

            LOADED_MODELS[name] = {
                "model": model,
                "scaler": scaler,
                "type": cfg["type"]
            }

        print(f"✓ Loaded {name}")

    print("\nAll models loaded successfully")


def get_model(model_name):

    if model_name not in LOADED_MODELS:

        raise ValueError(
            f"{model_name} not loaded"
        )

    return LOADED_MODELS[model_name]