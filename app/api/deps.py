from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db():
    """
    Dependency function to get a DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()