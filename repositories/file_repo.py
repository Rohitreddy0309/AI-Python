"""
Repository layer for file-related database operations.

This module provides functions to create a file record and update
the processing status of uploaded files in the database.
"""

from sqlalchemy.orm import Session

from models.file_data import FileData


def create_file_record(db: Session, file_data: dict):
    """
    Create a new file record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        file_data (dict): Dictionary containing file metadata.

    Returns:
        FileData: The created file record.
    """

    file = FileData(**file_data)

    db.add(file)
    db.commit()
    db.refresh(file)

    return file


def update_file_status(db: Session, file_id: int, status: str, result=None):
    """
    Update the processing status and parsed result of a file.

    Args:
        db (Session): SQLAlchemy database session.
        file_id (int): ID of the file record.
        status (str): Current processing status of the file.
        result (str, optional): Parsed result or error message.
    """

    file = db.query(FileData).filter(FileData.id == file_id).first()

    if file:
        file.upload_status = status
        file.parsed_result = result
        db.commit()
