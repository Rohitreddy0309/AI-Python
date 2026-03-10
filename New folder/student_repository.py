from typing import List, Optional

from sqlalchemy.orm import Session
from student_model import Student
from student_schema import StudentCreateSchema


class StudentRepository:
    """
    Handles database operations for Student
    """

    def create(self, db: Session, student_data: StudentCreateSchema) -> Student:
        student = Student(**student_data.model_dump())
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def get_all(self, db: Session) -> List[Student]:
        return db.query(Student).all()

    def get_by_id(self, db: Session, student_id: int) -> Optional[Student]:
        return db.query(Student).filter(Student.id == student_id).first()

    def delete(self, db: Session, student: Student) -> None:
        db.delete(student)
        db.commit()
