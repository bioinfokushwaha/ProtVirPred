import torch
import esm
import numpy as np
import re

from transformers import (
    T5Tokenizer,
    T5EncoderModel
)

from app.services.device_service import (
    DEVICE
)

import app.services.embedding_service as embedding_service


def generate_esm2_embeddings_batch(
    sequences
):

    batch_converter = (
        embedding_service.ESM_ALPHABET.get_batch_converter()
    )

    fasta_data = []

    for i, seq in enumerate(sequences):

        fasta_data.append(
            (
                f"seq_{i}",
                seq
            )
        )

    _, _, tokens = (
        batch_converter(
            fasta_data
        )
    )

    tokens = tokens[:, :1022].to(
        DEVICE
    )

    with torch.no_grad():

        outputs = embedding_service.ESM_MODEL(
            tokens,
            repr_layers=[33]
        )

    representations = (
        outputs["representations"][33]
    )

    embeddings = []

    for i, seq in enumerate(sequences):

        seq_len = min(
            len(seq),
            1022
        )

        emb = (
            representations[
                i,
                1:seq_len+1
            ]
            .mean(0)
            .cpu()
            .numpy()
        )

        embeddings.append(
            emb
        )

    return np.array(
        embeddings
    )

def generate_prott5_embeddings_batch(
    sequences
):

    processed_sequences = []

    for seq in sequences:

        processed_sequences.append(
            " ".join(
                list(
                    re.sub(
                        r"[UZOB]",
                        "X",
                        seq
                    )
                )
            )
        )

    inputs = (
        embedding_service.PROTT5_TOKENIZER(
            processed_sequences,
            padding=True,
            truncation=True,
            max_length=1022,
            return_tensors="pt"
        )
    )

    input_ids = (
        inputs["input_ids"]
        .to(DEVICE)
    )

    attention_mask = (
        inputs["attention_mask"]
        .to(DEVICE)
    )

    with torch.no_grad():

        outputs = embedding_service.PROTT5_MODEL(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

    hidden_states = (
        outputs.last_hidden_state
    )

    embeddings = []

    for i in range(
        len(sequences)
    ):

        seq_len = (
            attention_mask[i]
            .sum()
            .item()
        )

        emb = (
            hidden_states[
                i,
                :seq_len-1
            ]
            .mean(dim=0)
            .cpu()
            .numpy()
        )

        embeddings.append(
            emb
        )

    return np.array(
        embeddings
    )