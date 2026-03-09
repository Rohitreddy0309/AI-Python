"""
Database configuration module.

This module initializes the SQLAlchemy engine, session factory,
and base class for ORM models. It also provides the database
dependency used in FastAPI routes.
"""

# pylint: disable=invalid-name

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session.

    It creates a new database session for each request and
    ensures the session is closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

