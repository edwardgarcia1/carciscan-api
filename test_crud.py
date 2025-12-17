# This script is for development and testing purposes.

import sys
import os

from app.db.session import SessionLocal
from app.crud.carciscan import get_cid_by_synonym, get_smiles_by_cid


def test_database_connection():
    """
    Tests the CRUD functions against the database.
    """
    print("--- Testing Database Connection and CRUD Functions ---")

    # Create a database session
    db = SessionLocal()

    try:
        # --- Test 1: Get CID from a known synonym ---
        test_synonym = "Acetyl carnitine"
        print(f"\n[TEST 1] Searching for CID with synonym: '{test_synonym}'")

        cid = get_cid_by_synonym(db, test_synonym)

        if cid:
            print(f"✅ SUCCESS: Found CID -> {cid}")

            # --- Test 2: Get SMILES using the CID we just found ---
            print(f"\n[TEST 2] Searching for SMILES with CID: {cid}")
            smiles = get_smiles_by_cid(db, cid)

            if smiles:
                print(f"✅ SUCCESS: Found SMILES -> {smiles}")
            else:
                print(f"❌ FAILURE: Could not find SMILES for CID {cid}")
        else:
            print(f"❌ FAILURE: Could not find CID for synonym '{test_synonym}'")

        # --- Test 3: Test a case that should fail ---
        print(f"\n[TEST 3] Searching for a non-existent synonym: 'Fake Ingredient'")
        cid_fail = get_cid_by_synonym(db, "Fake Ingredient")
        if cid_fail is None:
            print("✅ SUCCESS: Correctly returned None for a non-existent synonym.")
        else:
            print(f"❌ FAILURE: Expected None, but got CID -> {cid_fail}")

    except Exception as e:
        print(f"\n❌ An unexpected error occurred during testing: {e}")
    finally:
        # Always close the session
        db.close()
        print("\n--- Database session closed. ---")


if __name__ == "__main__":
    test_database_connection()