import torch
import esm
import numpy as np
import re
import gc

from transformers import (
    T5Tokenizer,
    T5EncoderModel
)
from app.services.embedding_service import (
    ESM_MODEL,
    PROTT5_MODEL
)
from app.services.device_service import (
    DEVICE
)
import app.services.embedding_service as embedding_service

BATCH_SIZE = 8

def clear_gpu_memory():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    gc.collect()

def generate_esm2_embeddings_batch(
    sequences
):
    embedding_service.ESM_MODEL.to(DEVICE)
    batch_converter = (
        embedding_service.ESM_ALPHABET.get_batch_converter()
    )
    
    all_embeddings = []
    for start in range(0, len(sequences), BATCH_SIZE):
        batch_sequences = sequences[start:start+BATCH_SIZE]
        fasta_data = []

        for i, seq in enumerate(batch_sequences):
            fasta_data.append(
                (
                    f"seq_{start+i}",
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

        with torch.inference_mode():
            outputs = embedding_service.ESM_MODEL(
                tokens,
                repr_layers=[33]
            )

        representations = (
            outputs["representations"][33]
        )

        for i, seq in enumerate(batch_sequences):
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

            all_embeddings.append(
                emb
            )
            
        del tokens
        del outputs
        del representations
        clear_gpu_memory()

    embedding_service.ESM_MODEL.to( "cpu" )
    clear_gpu_memory()

    return np.array(
        all_embeddings, dtype=np.float32
    )

def generate_prott5_embeddings_batch(
    sequences
):
    embedding_service.PROTT5_MODEL.to(DEVICE)
    all_embeddings = []
    for start in range(0, len(sequences), BATCH_SIZE):
        batch_sequences = sequences[start:start+BATCH_SIZE]
        processed_sequences = []

        for seq in batch_sequences:
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

        with torch.inference_mode():
            outputs = embedding_service.PROTT5_MODEL(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

        hidden_states = (
            outputs.last_hidden_state
        )

        for i in range(
            len(batch_sequences)
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

            all_embeddings.append(
                emb
            )
            
        del inputs
        del input_ids
        del attention_mask
        del outputs
        del hidden_states
        clear_gpu_memory()
    
    embedding_service.PROTT5_MODEL.to("cpu")
    clear_gpu_memory()
    
    return np.array(
        all_embeddings, dtype=np.float32
    )