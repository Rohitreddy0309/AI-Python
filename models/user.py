"""
SQLAlchemy model for storing user information.

This model represents the users table in the database and contains
fields related to user identity, department, account status,
creation timestamp, and optional profile photo.
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from core.database import base


class User(base):
    """
    Database model representing a user.

    Stores user profile information such as name, email,
    department, active status, creation date, and photo path.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    department = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    photo = Column(String, nullable=True)
