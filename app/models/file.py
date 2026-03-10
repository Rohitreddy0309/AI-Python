"""
File database model.

Represents the uploaded files stored in the system.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class File(Base):
    """
    SQLAlchemy model for the 'files' table.

    Attributes:
        id (int): Unique identifier for the file
        filename (str): Name of the uploaded file
        filepath (str): Location where the file is stored
        status (str): Processing status of the file
    """

    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    status = Column(String)
