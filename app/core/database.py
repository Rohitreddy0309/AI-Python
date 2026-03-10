"""
Database configuration module.

This module sets up the SQLAlchemy engine, session factory,
and base model for the application. It also provides a dependency
function to get a database session for API requests.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency function that provides a database session.

    This function is used in FastAPI endpoints with Depends()
    to get a database session. The session is automatically
    closed after the request is completed.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
