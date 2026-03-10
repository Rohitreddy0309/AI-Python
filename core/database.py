"""
Database configuration and session management.

This module initializes the SQLAlchemy engine, base model class,
and session factory. It also provides a dependency function to
safely create and close database sessions.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
base = declarative_base()

db_url = os.getenv("db_url")
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Provide a database session for dependency injection.

    This generator yields a SQLAlchemy session and ensures that
    the session is properly closed after the request is completed.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
