from typing import Generator, List

from database import SessionLocal, engine
from sqlalchemy.orm import Session
from student_model import Base
from student_schema import StudentCreateSchema, StudentResponseSchema
from student_service import StudentService

from fastapi import Depends, FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student CRUD API")

student_service = StudentService()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=StudentResponseSchema)
def create_student(student: StudentCreateSchema, db: Session = Depends(get_db)):
    return student_service.create_student(db, student)


@app.get("/students/", response_model=List[StudentResponseSchema])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_students(db)


@app.get("/students/{student_id}", response_model=StudentResponseSchema)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return student_service.get_student(db, student_id)


@app.put("/students/{student_id}", response_model=StudentResponseSchema)
def update_student(
    student_id: int, student: StudentCreateSchema, db: Session = Depends(get_db)
):
    return student_service.update_student(db, student_id, student)


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_service.delete_student(db, student_id)
    return {"message": "Student deleted successfully"}
