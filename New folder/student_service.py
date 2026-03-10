from typing import List

from sqlalchemy.orm import Session
from student_model import Student
from student_repository import StudentRepository
from student_schema import StudentCreateSchema

from fastapi import HTTPException


class StudentService:
    """
    Business logic for Student.
    """

    def __init__(self) -> None:
        self.repository = StudentRepository()

    def create_student(self, db: Session, student_data: StudentCreateSchema) -> Student:
        return self.repository.create(db, student_data)

    def get_students(self, db: Session) -> List[Student]:
        return self.repository.get_all(db)

    def get_student(self, db: Session, student_id: int) -> Student:
        student = self.repository.get_by_id(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Stuent not found")
        return student

    def update_student(
        self, db: Session, student_id: int, student_data: StudentCreateSchema
    ) -> Student:
        student = self.get_student(db, student_id)

        student.name = student_data.name
        student.age = student_data.age
        student.marks = student_data.marks

        db.commit()
        db.refresh(student)

        return student

    def delete_student(self, db: Session, student_id: int) -> None:
        student = self.get_student(db, student_id)
        self.repository.delete(db, student)
