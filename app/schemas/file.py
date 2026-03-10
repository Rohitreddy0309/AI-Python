"""
file_schema.py

This module defines Pydantic schemas for File objects used in API responses.
The FileResponse schema represents a file's metadata returned to clients.
"""

from pydantic import BaseModel


class FileResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Schema for returning file information in API responses.

    Attributes:
        id (int): Unique identifier of the file.
        filename (str): Name of the file.
        filepath (str): Path where the file is stored.
    """

    id: int
    filename: str
    filepath: str

    class Config:  # pylint: disable=too-few-public-methods
        """
        Pydantic model configuration.

        Attributes:
            from_attributes (bool): Allows population of this schema from ORM model attributes.
        """

        from_attributes = True

    def __repr__(self) -> str:
        """Return string representation of FileResponse."""
        return f"FileResponse(id={self.id}, filename={self.filename!r}, filepath={self.filepath!r})"
