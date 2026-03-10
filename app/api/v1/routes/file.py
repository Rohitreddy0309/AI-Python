"""
File API Routes.

This module contains API endpoints for uploading, listing,
and deleting files. It also applies rate limiting to control
API usage.
"""

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.file import FileResponse
from app.services.file_service import FileService
from app.utils.rate_limiter import rate_limiter
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter()
file_service = FileService()


def get_db():
    """
    Provides a database session for each request.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/upload", response_model=FileResponse, dependencies=[Depends(rate_limiter)]
)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a file to the server.

    Args:
        file (UploadFile): File uploaded by the user
        db (Session): Database session

    Returns:
        FileResponse: Metadata of the uploaded file
    """
    db_file = await file_service.save_file(db, file)
    return db_file


@router.get("/files", response_model=list[FileResponse])
def get_files(db: Session = Depends(get_db)):
    """
    Retrieve all uploaded files.

    Args:
        db (Session): Database session

    Returns:
        List[FileResponse]: List of uploaded files
    """
    return file_service.get_files(db)


@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """
    Delete a file by its ID.

    Args:
        file_id (int): ID of the file
        db (Session): Database session

    Returns:
        dict: Confirmation message
    """
    return file_service.delete_file(db, file_id)
