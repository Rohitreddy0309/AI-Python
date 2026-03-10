"""
file_repository.py

This module defines the FileRepository class which provides CRUD operations
for the File model using SQLAlchemy sessions. It handles creating, retrieving,
and deleting file records in the database.
"""

from sqlalchemy.orm import Session

from app.models.file import File


class FileRepository:
    """
    Repository class for interacting with the File model in the database.

    Methods:
        create_file(db, file_id, filename, filepath): Creates a new file record.
        get_all_files(db): Retrieves all file records.
        get_file(db, file_id): Retrieves a single file record by its ID.
        delete_file(db, file): Deletes a specified file record.
    """

    def __repr__(self) -> str:
        """Return string representation of FileRepository."""
        return "FileRepository()"

    def create_file(self, db: Session, file_id: int, filename: str, filepath: str):
        """
        Create a new file record in the database.

        Args:
            db (Session): SQLAlchemy database session.
            file_id (int): Unique ID for the file.
            filename (str): Name of the file.
            filepath (str): Path where the file is stored.

        Returns:
            File: The newly created File object.
        """
        db_file = File(id=file_id, filename=filename, filepath=filepath)

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file

    def get_all_files(self, db: Session):
        """
        Retrieve all file records from the database.

        Args:
            db (Session): SQLAlchemy database session.

        Returns:
            List[File]: List of all File objects.
        """
        return db.query(File).all()

    def get_file(self, db: Session, file_id: int):
        """
        Retrieve a single file record by its ID.

        Args:
            db (Session): SQLAlchemy database session.
            file_id (int): Unique ID of the file to retrieve.

        Returns:
            File | None: The File object if found, else None.
        """
        return db.query(File).filter(File.id == file_id).first()

    def delete_file(self, db: Session, file):
        """
        Delete a specified file record from the database.

        Args:
            db (Session): SQLAlchemy database session.
            file (File): The File object to delete.

        Returns:
            None
        """
        db.delete(file)
        db.commit()
