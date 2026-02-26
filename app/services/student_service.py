from sqlalchemy.orm import Session
from app.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentUpdate
from app.utils.exceptions import ConflictException, NotFoundException 


class StudentService:
    """Business logic for Student."""

    def __init__(self) -> None:
        self.repository = StudentRepository()

    def create_student(self, db: Session, data: StudentCreate) -> Student:
        """Create a new student, rejecting duplicate emails."""
        existing_student = self.repository.get_by_email(db, data.email)
        if existing_student:
            raise ConflictException("Email already exists")

        student = Student(
            name=data.name,
            email=data.email,
        )
        return self.repository.create(db, student)

    def get_student(self, db: Session, student_id: int) -> Student:
        """Fetch a student by ID or raise 404."""
        student = self.repository.get_by_id(db, student_id)
        if not student:
            raise NotFoundException("Student not found")
        return student

    def list_students(self, db: Session) -> list[Student]:
        """Return all students."""
        return self.repository.get_all(db)

    def update_student(
        self,
        db: Session,
        student_id: int,
        data: StudentUpdate,
    ) -> Student:
        """Partially update a student's name or active status."""
        student = self.get_student(db, student_id)

        if data.name is not None:
            student.name = data.name

        if data.is_active is not None:
            student.is_active = data.is_active

        return self.repository.update(db, student)

    def delete_student(self, db: Session, student_id: int) -> None:
        """Soft delete — sets is_active to False."""
        student = self.get_student(db, student_id)
        student.is_active = False
        self.repository.update(db, student)