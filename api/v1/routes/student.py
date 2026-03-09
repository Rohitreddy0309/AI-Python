"""
Student API routes.

Handles CRUD operations and file uploads for students.
"""

# Standard library
import os
from typing import Union, List

# Third-party
from fastapi import APIRouter, Depends, status, UploadFile, File, Query, BackgroundTasks

# Local imports
from utils.rate_limiter import rate_limiter
from api.v1.dependencies import get_student_service
from schemas.student import StudentCreate, StudentResponse, StudentUpdate
from services.student_service import StudentService

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


@router.post("", response_model=list[StudentResponse], status_code=status.HTTP_201_CREATED)
def create_student(
    data: Union[StudentCreate, List[StudentCreate]],
    service: StudentService = Depends(get_student_service),
):
    """Create one or multiple students."""
    if isinstance(data, list):
        return service.create_students(data)
    return service.create_students([data])


@router.put("", response_model=List[StudentResponse])
def update_students(
    data: List[StudentUpdate],
    service: StudentService = Depends(get_student_service),
):
    """Update multiple students."""
    return service.update_students(data)


@router.get("", response_model=List[StudentResponse])
def list_students(
    service: StudentService = Depends(get_student_service),
):
    """Return all students."""
    return service.list_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    """Get a single student by ID."""
    return service.get_student(student_id)


@router.delete("")
def delete_students(
    students_ids: List[int] = Query(...),
    service: StudentService = Depends(get_student_service),
):
    """Delete multiple students."""
    service.delete_students(students_ids)
    return {"message": "Students deleted successfully"}


@router.post("/{student_id}/upload", dependencies=[Depends(rate_limiter)])
async def upload_file(
    student_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    service: StudentService = Depends(get_student_service),
):
    """Upload a file for a student and process it in background."""

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    service.save_uploaded_file(student_id, file.filename)

    background_tasks.add_task(service.process_student_file, student_id)

    return service.get_student(student_id)
