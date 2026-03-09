"""
Student repository module.

Handles database operations related to Student entities.
"""

from sqlalchemy.orm import Session

from models.student import Student


class StudentRepository:
    """Database access layer for Student."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    # ---------------- CREATE ----------------

    def create_many(self, students: list[Student]):
        """Insert multiple students into the database."""
        self.db.add_all(students)
        self.db.commit()

        for student in students:
            self.db.refresh(student)

        return students

    # ---------------- READ ----------------

    def get_all(self):
        """Retrieve all students."""
        return self.db.query(Student).all()

    def get_by_id(self, student_id: int):
        """Retrieve a student by ID."""
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_by_ids(self, ids: list[int]):
        """Retrieve multiple students by IDs."""
        return self.db.query(Student).filter(Student.id.in_(ids)).all()

    def get_all_active(self):
        """Retrieve all active students."""
        return self.db.query(Student).filter(Student.is_active.is_(True)).all()

    def get_by_email(self, email: str):
        """Retrieve a student by email."""
        return self.db.query(Student).filter(Student.email == email).first()

    # ---------------- UPDATE ----------------

    def update_many(self, students: list[Student]):
        """Update multiple student records."""
        self.db.commit()

        for student in students:
            self.db.refresh(student)

        return students
