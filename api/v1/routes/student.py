from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from typing import Union, List
from fastapi import Query
from schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from services.student_service import StudentService

router = APIRouter()
service = StudentService()


# -------------------- CREATE --------------------

@router.post(
    "",
    response_model=list[StudentResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    data: Union[StudentCreate, List[StudentCreate]],
    db: Session = Depends(get_db),
):
    if isinstance(data,list):
        return service.create_students(db, data)
    return service.create_students(db,[data])



# -------------------- UPDATE --------------------

@router.put(
    "",
    response_model=List[StudentResponse],
)
def update_students(
    data: Union[StudentUpdate, List[StudentUpdate]],
    db: Session = Depends(get_db),
):
    if isinstance(data, list):
        return service.update_students(db, data)
    return service.update_students(db, [data])

# -------------------- READ --------------------

@router.get("", response_model=List[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return service.list_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return service.get_student(db, student_id)
  


# -------------------- DELETE --------------------


@router.delete("")
def delete_students(
    students_ids: List[int] = Query(...),
    db: Session = Depends(get_db),
):
    service.delete_students(db, students_ids)
    return {"message": "Students deleted successfully"}