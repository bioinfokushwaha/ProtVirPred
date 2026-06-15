from app.services.error_handler import (
    raise_validation_error
)

from app.config import (
    MIN_SEQUENCE_LENGTH,
    MAX_SEQUENCE_LENGTH
)

VALID_AMINO_ACIDS = set(
    "ACDEFGHIKLMNPQRSTVWY"
)


def validate_sequence(
    sequence: str
):

    sequence = (
        sequence.strip()
        .upper()
    )

    if len(sequence) == 0:

        raise_validation_error(
            "Empty sequence"
        )

    if len(sequence) < MIN_SEQUENCE_LENGTH:

        raise_validation_error(
            f"Sequence must contain at least "
            f"{MIN_SEQUENCE_LENGTH} amino acids"
        )

    if len(sequence) > MAX_SEQUENCE_LENGTH:

        raise_validation_error(
            f"Sequence exceeds maximum length "
            f"({MAX_SEQUENCE_LENGTH})"
        )

    invalid = (
        set(sequence)
        - VALID_AMINO_ACIDS
    )

    if invalid:

        raise_validation_error(
            f"Invalid amino acids found: {invalid}"
        )

    return sequence


def validate_sequences(
    sequences
):

    validated = []

    for seq in sequences:

        validated.append(
            validate_sequence(seq)
        )

    return validated