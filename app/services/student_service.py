
from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from fastapi import HTTPException


class StudentService:


    def __init__(self):
        
        self.repository = StudentRepository()

    def __repr__(self) -> str:

        return "StudentService()"

    def create_student(self, db: Session, name: str, age: int, marks: int):
        
        return self.repository.create_student(db, name, age, marks)

    def get_students(self, db: Session):
        
        return self.repository.get_all_students(db)

    def get_student(self, db: Session, student_id: int):
        
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    def get_student_by_id(self, db: Session, student_id: int):
        
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    def update_student(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self, db: Session, student_id: int, name: str, age: int, marks: int
    ):
        
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return self.repository.update_student(db, student, name, age, marks)

    def delete_student(self, db: Session, student_id: int):
        
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        self.repository.delete_student(db, student)
        return {"message": "Student deleted successfully"}
