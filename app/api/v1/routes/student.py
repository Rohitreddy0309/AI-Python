from app.api.v1.routes.file import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["Students"])

student_service = StudentService()


@router.post("/")
def create_student(name: str, age: int, marks: int, db: Session = Depends(get_db)):
    return student_service.create_student(db, name, age, marks)


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return student_service.get_students(db)

@router.get("/{student_id}")
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    return student_service.get_student_by_id(db, student_id)


@router.put("/{student_id}")
def update_student(student_id: int, name: str, age: int, marks: int, db: Session = Depends(get_db)):
    return student_service.update_student(db, student_id, name, age, marks)


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return student_service.delete_student(db, student_id)