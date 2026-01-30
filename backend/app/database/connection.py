"""SQLAlchemy database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from ..config import get_settings, ensure_data_dir

settings = get_settings()

# Ensure data directory exists before creating engine
ensure_data_dir()

# Create SQLAlchemy engine
# SQLite specific: check_same_thread=False allows multiple threads
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from ..models.db_models import Base
    Base.metadata.create_all(bind=engine)
