import torch
import esm
import numpy as np
import re

from transformers import (
    T5Tokenizer,
    T5EncoderModel
)

from app.services.device_service import (
    DEVICE,
    get_device_name
)

ESM_MODEL = None
ESM_ALPHABET = None
BATCH_CONVERTER = None

PROTT5_MODEL = None
PROTT5_TOKENIZER = None

def load_esm2():
    
    global ESM_MODEL
    global ESM_ALPHABET
    global BATCH_CONVERTER

    print(f"Loading ESM2 on {get_device_name()}...")

    ESM_MODEL, ESM_ALPHABET = (
        esm.pretrained.esm2_t33_650M_UR50D()
    )

    ESM_MODEL.eval()

    ESM_MODEL.to(
        DEVICE
    )

    BATCH_CONVERTER = (
        ESM_ALPHABET.get_batch_converter()
    )

    print("✓ ESM2 Loaded")

def load_prott5():
    
    global PROTT5_MODEL
    global PROTT5_TOKENIZER

    print(
        f"Loading ProtT5 on {get_device_name()}..."
    )

    print("Loading ProtT5 tokenizer...")
    
    PROTT5_TOKENIZER = (
        T5Tokenizer.from_pretrained(
            "Rostlab/prot_t5_xl_uniref50"
        )
    )
    print("✓ ProtT5 tokenizer loaded")
    print("Loading ProtT5 model...")
    PROTT5_MODEL = (
        T5EncoderModel.from_pretrained(
            "Rostlab/prot_t5_xl_uniref50"
        )
    )
    print("✓ ProtT5 model loaded")
    PROTT5_MODEL.eval()
    print("Moving ProtT5 to GPU...")
    PROTT5_MODEL.to(
        DEVICE
    )
    print("✓ ProtT5 Loaded")

def load_embedding_models():    
    load_esm2()
    load_prott5()
    
def generate_esm2_embedding(sequence):

    fasta_data = [
        ("protein", sequence)
    ]

    _, _, tokens = BATCH_CONVERTER(
        fasta_data
    )

    tokens = tokens[:, :1022].to(DEVICE)

    with torch.no_grad():

        results = ESM_MODEL(
            tokens,
            repr_layers=[33],
            return_contacts=False
        )

    actual_len = min(
        len(sequence),
        1022
    )

    token_repr = results[
        "representations"
    ][33]

    embedding = (
        token_repr[
            0,
            1:actual_len+1
        ]
        .mean(0)
        .cpu()
        .numpy()
    )

    return embedding
    
def generate_prott5_embedding(sequence):

    sequence = " ".join(
        list(
            re.sub(
                r"[UZOB]",
                "X",
                sequence
            )
        )
    )

    inputs = PROTT5_TOKENIZER(
        sequence,
        add_special_tokens=True,
        padding="longest",
        truncation=True,
        max_length=1022,
        return_tensors="pt"
    )

    input_ids = inputs[
        "input_ids"
    ].to(DEVICE)

    attention_mask = inputs[
        "attention_mask"
    ].to(DEVICE)

    with torch.no_grad():

        outputs = PROTT5_MODEL(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

    last_hidden = outputs.last_hidden_state

    actual_len = (
        attention_mask[0] == 1
    ).sum().item()

    embedding = (
        last_hidden[
            0,
            :actual_len-1
        ]
        .mean(dim=0)
        .cpu()
        .numpy()
    )

    return embedding