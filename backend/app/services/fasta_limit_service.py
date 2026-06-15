from app.config import (
    MAX_FASTA_SEQUENCES,
    MAX_FASTA_FILE_SIZE_MB
)

from app.services.error_handler import (
    raise_validation_error
)


def validate_fasta_sequence_count(
    proteins
):

    if len(proteins) > MAX_FASTA_SEQUENCES:

        raise_validation_error(
            f"Maximum {MAX_FASTA_SEQUENCES} sequences allowed"
        )


def validate_fasta_file_size(
    size_bytes
):

    max_bytes = (
        MAX_FASTA_FILE_SIZE_MB
        * 1024
        * 1024
    )

    if size_bytes > max_bytes:

        raise_validation_error(
            f"File exceeds {MAX_FASTA_FILE_SIZE_MB} MB limit"
        )