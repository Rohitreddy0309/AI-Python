import os
from models.student import Student
from repositories.student_repository import StudentRepository
from schemas.student import StudentCreate, StudentUpdate
from utils.exceptions import ConflictException, NotFoundException

UPLOAD_DIR = "uploads"


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

# ---------------- CREATE ----------------

    def create_students(self, data: list[StudentCreate]):
        students = []

        for item in data:
            existing = self.repository.get_by_email(item.email)

            if existing:
                raise ConflictException("Email already exists")

            student = Student(
                name=item.name,
                email=item.email,
            )

            students.append(student)

        return self.repository.create_many(students)

# ---------------- READ ----------------

    def list_students(self):
        return self.repository.get_all_active()

    def get_student(self, student_id: int):
        student = self.repository.get_by_id(student_id)

        if not student:
            raise NotFoundException("Student not found")

        return student

# ---------------- UPDATE ----------------

    def update_students(self, data: list[StudentUpdate]):
        updated_students = []

        for item in data:
            student = self.repository.get_by_id(item.id)

            if not student:
                raise NotFoundException("Student not found")

            if item.name is not None:
                student.name = item.name

            if item.is_active is not None:
                student.is_active = item.is_active

            updated_students.append(student)

        return self.repository.update_many(updated_students)

# ---------------- DELETE ----------------

    def delete_students(self, ids: list[int]):
        students = self.repository.get_by_ids(ids)

        if not students:
            raise NotFoundException("Student not found")

        for student in students:
            student.is_active = False

        self.repository.update_many(students)

# ---------------- FILE PROCESSING ----------------

    def process_student_file(self, student_id: int):

        student = self.repository.get_by_id(student_id)

        if not student:
            return

        student.status = "PROCESSING"
        self.repository.update_many([student])

        file_path = os.path.join(UPLOAD_DIR, student.file_name)

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            student.status = "COMPLETED"
            student.result = "Processing completed"

        except Exception as e:
            student.status = "FAILED"
            student.result = str(e)

        self.repository.update_many([student])