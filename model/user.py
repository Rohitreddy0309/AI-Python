"""
Plant database model.

This module defines the SQLAlchemy ORM model for the plants table,
which stores plant information including watering schedule,
sunlight requirements, and uploaded file processing details.
"""

from sqlalchemy import Column, DateTime, Integer, String, Text

from core.database import Base


# pylint: disable=too-few-public-methods
class Plant(Base):
    """SQLAlchemy ORM model representing a plant record."""

    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    watering_interval_days = Column(Integer, nullable=False)
    sunlight = Column(String, nullable=False)
    last_watered = Column(DateTime(timezone=True), nullable=False)
    file_path = Column(String, nullable=True)
    file_status = Column(String, nullable=True)
    file_result = Column(Text, nullable=True)
  