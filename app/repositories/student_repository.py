from sqlalchemy.orm import Session
from app.models.student import Student  


class StudentRepository:
    """Database access layer for Student."""

    def create(self, db: Session, student: Student) -> Student:
        """Add a new student to the database."""
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def get_by_id(self, db: Session, student_id: int) -> Student | None:
        """Fetch a single student by primary key."""
        return db.query(Student).filter(Student.id == student_id).first()

    def get_by_email(self, db: Session, email: str) -> Student | None:
        """Fetch a student by email address."""
        return db.query(Student).filter(Student.email == email).first()

    def get_all(self, db: Session) -> list[Student]:
        """Fetch all students."""
        return db.query(Student).all()

    def update(self, db: Session, student: Student) -> Student:
        """Persist changes to an existing student."""
        db.commit()
        db.refresh(student)
        return student