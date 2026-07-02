import numpy as np

from app.services.embedding_service import (
    generate_esm2_embedding,
    generate_prott5_embedding
)

from app.services.physchem_service import (
    calculate_physchem_features
)

def build_features(
    sequence,
    combination
):

    physchem = np.array(
        calculate_physchem_features(
            sequence
        )
    )

    if combination == "esm2_only":

        return generate_esm2_embedding(
            sequence
        )

    elif combination == "prott5_only":

        return generate_prott5_embedding(
            sequence
        )

    elif combination == "esm2_physchem":

        esm = generate_esm2_embedding(
            sequence
        )

        return np.concatenate(
            [physchem, esm]
        )

    elif combination == "prott5_physchem":

        t5 = generate_prott5_embedding(
            sequence
        )

        return np.concatenate(
            [physchem, t5]
        )

    elif combination == "esm2_prott5":

        esm = generate_esm2_embedding(
            sequence
        )

        t5 = generate_prott5_embedding(
            sequence
        )

        return np.concatenate(
            [esm, t5]
        )

    elif combination == "esm2_prott5_physchem":

        esm = generate_esm2_embedding(
            sequence
        )

        t5 = generate_prott5_embedding(
            sequence
        )

        return np.concatenate([
            physchem,
            esm,
            t5
        ])
        

    raise ValueError(
        f"Unknown combination: {combination}"
    )