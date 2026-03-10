"""
Database configuration and session management.

This module initializes the SQLAlchemy engine, session factory,
and base class for ORM models. It also provides a database
dependency used in FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # pylint: disable=invalid-name

Base = declarative_base()


def get_db():
    """
    Provide a database session for dependency injection.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
