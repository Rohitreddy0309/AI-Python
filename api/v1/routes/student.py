import os
import uuid
from typing import Union, List
from core.database import get_db
from models.student import Student
from sqlalchemy.orm import Session
from utils.rate_limiter import rate_limiter
from api.v1.dependencies import get_student_service
from utils.exceptions import ConflictException, NotFoundException 
from fastapi import APIRouter, Depends, status,UploadFile, File, Query, BackgroundTasks


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


from schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from services.student_service import StudentService

router = APIRouter()



# -------------------- CREATE --------------------

@router.post(
    "",
    response_model=list[StudentResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    data: Union[StudentCreate, List[StudentCreate]],
    service: StudentService = Depends(get_student_service)
):
    if isinstance(data,list):
        return service.create_students(data)
    return service.create_students([data])



# -------------------- UPDATE --------------------

@router.put(
    "",
    response_model=List[StudentResponse],
)
def update_students(
    data: Union[StudentUpdate, List[StudentUpdate]],
    service: StudentService= Depends(get_student_service)
):
    if isinstance(data, list):
        return service.update_students(data)
    return service.update_students([data])

# -------------------- READ --------------------

@router.get("", response_model=List[StudentResponse])
def list_students(db: Session = Depends(get_db),
    service: StudentService = Depends(get_student_service)
):
    return service.list_students()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    return service.get_student(student_id)
  


# -------------------- DELETE --------------------


@router.delete("")
def delete_students(
    students_ids: List[int] = Query(...),
    service: StudentService = Depends(get_student_service)
):
    service.delete_students(students_ids)
    return {"message": "Students deleted successfully"}

# -------------------- FILE UPLOAD --------------------

@router.post("/{student_id}/upload", dependencies=[Depends(rate_limiter)])
async def upload_file(
    student_id: int,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    service: StudentService = Depends(get_student_service)
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    student = service.get_student(student_id)

    background_tasks.add_task(
        service.process_student_file,
        student.id
    )

    return student


