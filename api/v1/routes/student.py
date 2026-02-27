from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from services.student_service import StudentService

router = APIRouter()
service = StudentService()


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    return service.create_student(db, data)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return service.get_student(db, student_id)


@router.get("", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return service.list_students(db)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
):
    return service.update_student(db, student_id, data)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    service.delete_student(db, student_id)