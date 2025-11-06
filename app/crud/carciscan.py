from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
from sqlalchemy import text

# Import the SQLAlchemy models we defined earlier
from app.models.carciscan import Synonyms, Smiles

def get_cid_by_synonym(db: Session, synonym: str) -> Optional[int]:
    """
    Retrieves the CID for a given chemical synonym.

    Args:
        db: The SQLAlchemy database session.
        synonym: The chemical name to search for.

    Returns:
        The CID if found, otherwise None.
    """
    # We perform a case-insensitive search for an exact match.
    # Using .first() is efficient as we only need one result.
    db_synonym = db.query(Synonyms).filter(Synonyms.synonyms.ilike(synonym)).first()
    if db_synonym:
        return db_synonym.cid
    return None

def get_smiles_by_cid(db: Session, cid: int) -> Optional[str]:
    """
    Retrieves the SMILES string for a given CID.

    Args:
        db: The SQLAlchemy database session.
        cid: The chemical identifier.

    Returns:
        The SMILES string if found, otherwise None.
    """
    smiles_record = db.query(Smiles).filter(Smiles.cid == cid).first()
    if smiles_record:
        return smiles_record.smiles
    return None

# A helper function to get multiple potential CIDs if a synonym is ambiguous
def get_cids_by_synonym_partial(db: Session, synonym: str) -> List[int]:
    """
    Retrieves a list of CIDs for a partial synonym match.
    Useful for handling cases where the full name isn't found.

    Args:
        db: The SQLAlchemy database session.
        synonym: The partial chemical name to search for.

    Returns:
        A list of CIDs if any matches are found, otherwise an empty list.
    """
    db_synonyms = db.query(Synonyms).filter(Synonyms.synonyms.ilike(f"%{synonym}%")).all()
    return [s.cid for s in db_synonyms]


def find_cid_by_synonym_fuzzy(db: Session, search_term: str, score_cutoff: float = 0.90) -> Optional[
    Tuple[str, int, float]]:
    """
    Finds the best matching synonym using DuckDB's native jaro_winkler_similarity.
    This is extremely fast and efficient.

    Args:
        db: The SQLAlchemy database session.
        search_term: The ingredient name from OCR.
        score_cutoff: The minimum similarity score (0-1) to consider a match.

    Returns:
        A tuple of (matched_synonym, cid, score) if a good match is found, otherwise None.
    """
    # The text() construct allows us to write raw SQL while still protecting against injection
    # with parameterization (:search_term, :score_cutoff)
    sql_query = text("""
        SELECT 
            s.synonyms, 
            s.cid, 
            jaro_winkler_similarity(LOWER(s.synonyms), LOWER(:search_term)) AS score
        FROM synonyms s
        WHERE score >= :score_cutoff
        ORDER BY score DESC
        LIMIT 1
    """)

    # Execute the query with parameters
    result = db.execute(sql_query, {"search_term": search_term, "score_cutoff": score_cutoff}).fetchone()

    if result:
        # result is a tuple-like Row object: ('matched synonym', 123, 0.95)
        matched_synonym = result[0]
        cid = result[1]
        score = result[2]
        return matched_synonym, cid, score

    return None