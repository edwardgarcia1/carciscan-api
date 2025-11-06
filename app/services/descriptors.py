from rdkit import Chem
from rdkit.Chem import Descriptors
from typing import List, Optional, Dict


def calculate_rdkit_descriptors(smiles: str) -> Optional[Dict[str, float]]:
    """
    Calculates all available RDKit descriptors for a given SMILES string.
    Returns a dictionary of {descriptor_name: value}.
    """
    if not smiles:
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # CalcMolDescriptors returns a dictionary of {descriptor_name: value}
    descriptor_dict: Dict[str, float] = Descriptors.CalcMolDescriptors(mol)

    # DO NOT SORT HERE. Let the predictor handle alignment.
    # print(f"Calculated {len(descriptor_dict)} descriptors for SMILES: {smiles}")

    return descriptor_dict  # Return the dictionary directly


# --- Test Block ---
if __name__ == '__main__':
    # A valid SMILES string from our database
    valid_smiles = "CC(=O)OC(CC(=O)[O-])C[N+](C)(C)C"

    # An invalid SMILES string
    invalid_smiles = "C1=CC=CC=C1X"  # 'X' is not a valid atom in this context

    print(f"Testing with valid SMILES: {valid_smiles}")
    descriptors = calculate_rdkit_descriptors(valid_smiles)
    if descriptors:
        print(f"✅ SUCCESS: Calculated {len(descriptors)} descriptors.")
        print(f"First 5 descriptors: {descriptors[:5]}")
    else:
        print("❌ FAILURE: Could not calculate descriptors for a valid SMILES.")

    print("\n" + "=" * 40 + "\n")

    print(f"Testing with invalid SMILES: {invalid_smiles}")
    invalid_descriptors = calculate_rdkit_descriptors(invalid_smiles)
    if invalid_descriptors is None:
        print("✅ SUCCESS: Correctly returned None for an invalid SMILES.")
    else:
        print("❌ FAILURE: Should have returned None for an invalid SMILES.")