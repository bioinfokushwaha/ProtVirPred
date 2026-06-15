def parse_fasta(fasta_text: str):
    
    sequences = []

    seq_id = None
    seq_lines = []

    for line in fasta_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith(">"):

            if seq_id is not None:

                sequences.append(
                    (
                        seq_id,
                        "".join(seq_lines)
                    )
                )

            seq_id = line[1:]
            seq_lines = []

        else:

            seq_lines.append(line)

    if seq_id is not None:

        sequences.append(
            (
                seq_id,
                "".join(seq_lines)
            )
        )

    return sequences    