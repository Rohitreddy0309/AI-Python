from sqlalchemy.orm import Session
from models.student import Student


class StudentRepository:
    """Database access layer for Student."""

    def __init__(self, db: Session):
        self.db = db


# ---------------- CREATE ----------------

    def create_many(self, students: list[Student]):
        self.db.add_all(students)
        self.db.commit()
        for student in students:
            self.db.refresh(student)
        return students


# ---------------- READ ----------------

    def get_all(self):
        return self.db.query(Student).all()


    def get_by_id(self, student_id: int):
        return self.db.query(Student).filter(Student.id == student_id).first()


    def get_by_ids(self, ids: list[int]):
        return self.db.query(Student).filter(Student.id.in_(ids)).all()


    def get_all_active(self):
        return self.db.query(Student).filter(Student.is_active == True).all()


    def get_by_email(self, email: str):
        return self.db.query(Student).filter(Student.email == email).first()


# ---------------- UPDATE ----------------

    def update_many(self, students: list[Student]):
        self.db.commit()
        for student in students:
            self.db.refresh(student)
        return students