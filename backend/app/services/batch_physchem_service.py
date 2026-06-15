import numpy as np

from app.services.physchem_service import (
    calculate_physchem_features
)


def calculate_physchem_batch(
    sequences
):

    results = []

    for seq in sequences:

        features = calculate_physchem_features(
            seq
        )

        results.append(
            features
        )

    return np.array(results)