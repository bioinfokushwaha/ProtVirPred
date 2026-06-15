import numpy as np

from app.services.batch_embedding_service import (
    generate_esm2_embeddings_batch,
    generate_prott5_embeddings_batch
)

from app.services.batch_physchem_service import (
    calculate_physchem_batch
)


def build_batch_features(
    sequences,
    combination
):

    esm = generate_esm2_embeddings_batch(
        sequences
    )

    t5 = generate_prott5_embeddings_batch(
        sequences
    )

    physchem = calculate_physchem_batch(
        sequences
    )

    features = []

    for i in range(len(sequences)):

        if combination == "esm2_only":

            feature = esm[i]

        elif combination == "esm2_physchem":

            feature = np.concatenate(
                [
                    esm[i],
                    physchem[i]
                ]
            )

        elif combination == "prott5_only":

            feature = t5[i]

        elif combination == "prott5_physchem":

            feature = np.concatenate(
                [
                    t5[i],
                    physchem[i]
                ]
            )

        elif combination == "esm2_prott5":

            feature = np.concatenate(
                [
                    esm[i],
                    t5[i]
                ]
            )

        elif combination == "esm2_prott5_physchem":

            feature = np.concatenate(
                [
                    esm[i],
                    t5[i],
                    physchem[i]
                ]
            )

        else:

            raise ValueError(
                f"Invalid combination: {combination}"
            )

        features.append(feature)

    return np.array(features)