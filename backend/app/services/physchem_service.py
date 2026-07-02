from Bio.SeqUtils.ProtParam import ProteinAnalysis


def calculate_physchem_features(sequence):

    protein = ProteinAnalysis(sequence)

    return [
        len(sequence),                      # 1. length
        protein.molecular_weight(),         # 2. molecular weight
        protein.aromaticity(),              # 3. aromaticity
        protein.instability_index(),        # 4. instability index
        protein.isoelectric_point(),        # 5. isoelectric point
        protein.gravy(),                    # 6. GRAVY

        # Placeholder structural features
        # These should ideally be replaced with actual predicted values
        # if available, but must remain in this position.
        75.0,                              # 7. AlphaFold pLDDT
        550.0,                             # 8. Pocket volume
        15.0                               # 9. Pocket depth
    ]