"""
File database model.

Represents the uploaded files stored in the system.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class File(Base):  # pylint: disable=too-few-public-methods
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

    def __repr__(self) -> str:
        """Return string representation of File."""
        return f"File(id={self.id}, filename={self.filename!r}, filepath={self.filepath!r})"
