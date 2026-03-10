"""Database setup and session utilities."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session, closing it after use."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
