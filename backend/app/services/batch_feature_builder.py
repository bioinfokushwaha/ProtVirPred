import numpy as np
import gc

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
    esm = None 
    t5 = None
    if "esm2" in combination:
        esm = generate_esm2_embeddings_batch(
            sequences
        )
    if "prott5" in combination:
        t5 = generate_prott5_embeddings_batch(
            sequences
        )
    physchem = None
    if "physchem" in combination:
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
        
    del esm 
    del t5 
    del physchem 
    gc.collect()

    return np.array(features, dtype=np.float32)