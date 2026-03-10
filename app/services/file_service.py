"""
File service layer.

Contains business logic for file operations such as
saving, retrieving, and deleting files.
"""

import os

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.file import File
from app.repositories.file_repository import FileRepository
from app.utils.db_helpers import get_lowest_available_id
from fastapi import HTTPException, UploadFile


class FileService:
    """
    Handles business logic for file operations.
    """

    def __init__(self):
        self.repository = FileRepository()

    def __repr__(self) -> str:
        """Return string representation of FileService."""
        return "FileService()"

    async def save_file(self, db: Session, upload_file: UploadFile):
        """
        Save an uploaded file to disk and database.

        Args:
            db (Session): Database session
            upload_file (UploadFile): Uploaded file

        Returns:
            File: Stored file record
        """
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, upload_file.filename)

        contents = await upload_file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        new_id = get_lowest_available_id(db, File)

        db_file = self.repository.create_file(
            db, new_id, upload_file.filename, file_path
        )

        return db_file

    def get_files(self, db: Session):
        """
        Retrieve all files.

        Args:
            db (Session): Database session

        Returns:
            list: List of all files
        """
        return self.repository.get_all_files(db)

    def delete_file(self, db: Session, file_id: int):
        """
        Delete a file by ID.

        Args:
            db (Session): Database session
            file_id (int): ID of the file to delete

        Returns:
            dict: Deletion status message
        """
        db_file = self.repository.get_file(db, file_id)

        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")

        if os.path.exists(db_file.filepath):
            os.remove(db_file.filepath)

        self.repository.delete_file(db, db_file)

        return {"message": "File deleted successfully"}
