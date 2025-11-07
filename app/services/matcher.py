from typing import Tuple, Optional
from sqlalchemy.orm import Session

from app.crud.carciscan import find_cid_by_synonym_fuzzy


def find_best_synonym_match(search_term: str, db: Session, score_cutoff: float = 0.95) -> Optional[Tuple[str, int]]:
    """
    Finds the best matching synonym using the high-performance DuckDB function.
    """
    match_result = find_cid_by_synonym_fuzzy(db, search_term, score_cutoff)

    if match_result:
        # match_result is (matched_synonym, cid, score)
        matched_synonym, cid, score = match_result
        # We don't need the score in the final output, but it's good for logging
        print(f"DB Fuzzy Match: '{search_term}' -> '{matched_synonym}' (CID: {cid}, Score: {score:.2f})")
        return matched_synonym, cid

    return None