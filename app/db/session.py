from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the settings from our config file
from app.core.config import settings

# Create the SQLAlchemy engine
# The `connect_args` is NOT needed for DuckDB and causes an error.
engine = create_engine(
    settings.DATABASE_URL,
    # Removed: connect_args={"check_same_thread": False},
    echo=True # Set to True to see all SQL queries generated (good for debugging)
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a DB session
def get_db():
    """
    Dependency function that will be used in our API endpoints.
    It creates a new database session for each request and closes it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()