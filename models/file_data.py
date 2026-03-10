"""
SQLAlchemy model for storing uploaded file information.

This model represents metadata related to uploaded files,
including file details, processing status, and parsing results.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from core.database import base


class FileData(base):
    """
    Database model representing file upload metadata.

    Stores information about uploaded files, their processing status,
    and results generated after file parsing.
    """

    __tablename__ = "files_data"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)

    upload_status = Column(String, default="uploading")
    parsed_result = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
