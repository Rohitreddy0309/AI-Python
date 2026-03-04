import os
from sqlalchemy.orm import Session
from models.student import Student
from repositories.student_repository import StudentRepository
from schemas.student import StudentCreate, StudentUpdate
from utils.exceptions import ConflictException, NotFoundException 

UPLOAD_DIR = "uploads"

class StudentService:
    def __init__(self) -> None:
        self.repository = StudentRepository()

    #Create---------------------------------------------------

    def create_students(self, db: Session, data: list[StudentCreate]):
        students = []

        for item in data:
            existing = self.repository.get_by_email(db, item.email)

            if existing:
                raise ConflictException("Email already exists")

            student = Student(
                name=item.name,
                email=item.email,
            )

            students.append(student)

        return self.repository.create_many(db, students)
    
    #Read-----------------------------------------------------
    
    def list_students(self, db: Session):
        return self.repository.get_all_active(db)
    
    def get_student(self, db: Session, student_id: int):
        student = self.repository.get_by_id(db, student_id)
        if not student:
            raise NotFoundException("Student not found")
        return student

    #Update---------------------------------------------------

    def update_students(self, db: Session, data: list[StudentUpdate]):
        updated_students = []

        for item in data:
            student = self.repository.get_by_id(db, item.id)

            if not student:
                raise NotFoundException("Student not found")

            if item.name is not None:
                student.name = item.name

            if item.is_active is not None:
                student.is_active = item.is_active

            updated_students.append(student)

        return self.repository.update_many(db, updated_students)

    #Delete---------------------------------------------------------------

    def delete_students(self, db: Session, ids: list[int]):
        students = self.repository.get_by_ids(db, ids)

        if not students:
            raise NotFoundException("Student not found")

        for student in students:
            student.is_active = False

        self.repository.update_many(db, students)

    # File Processing ---------------------------------------------------

    def process_student_file(self, db: Session, student_id: int):
        """
        Background task to process uploaded student file.
        """

        student = self.repository.get_by_id(db, student_id)

        if not student:
            return

        student.status = "PROCESSING"
        self.repository.update_many(db, [student])   

        file_path = os.path.join(UPLOAD_DIR, student.file_name)

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            file_size = len(content)

            student.status = "COMPLETED"
            student.result = "Processing completed"

        except Exception as e:
            student.status = "FAILED"
            student.result = str(e)

        self.repository.update_many(db, [student])   