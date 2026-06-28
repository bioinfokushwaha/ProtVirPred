from Bio.SeqUtils.ProtParam import ProteinAnalysis

def calculate_physchem_features(sequence):

    protein = ProteinAnalysis(sequence)

    return [
        protein.molecular_weight(),
        protein.aromaticity(),
        protein.instability_index(),
        protein.isoelectric_point(),
        protein.gravy(),

        len(sequence),

        75.0,   # alphafold_plddt
        550.0,  # pocket_volume
        15.0    # pocket_depth
    ]