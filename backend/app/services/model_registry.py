MODEL_CONFIGS = {

    "esm2_only": {
        "type": "dnn",
        "path": "app/models/ESM2_only/model.pth",
        "input_dim": 1280
    },

    "esm2_physchem": {
        "type": "xgb",
        "path": "app/models/ESM2+Physchem/model.pkl",
        "input_dim": 1289
    },

    "prott5_only": {
        "type": "svm",
        "path": "app/models/ProtT5_only/model.pkl",
        "input_dim": 1024
    },

    "prott5_physchem": {
        "type": "dnn",
        "path": "app/models/ProtT5+Physchem/model.pth",
        "input_dim": 1033
    },

    "esm2_prott5": {
        "type": "svm",
        "path": "app/models/ESM2+ProtT5/model.pkl",
        "input_dim": 2304
    },

    "esm2_prott5_physchem": {
        "type": "dnn",
        "path": "app/models/ESM2+ProtT5+Physchem/model.pth",
        "input_dim": 2313
    }
}