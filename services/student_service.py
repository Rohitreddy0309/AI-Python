"""
Student service layer.

Handles business logic related to students such as
creation, updates, deletion, and file processing.
"""

import os

from models.student import Student
from repositories.student_repository import StudentRepository
from schemas.student import StudentCreate, StudentUpdate
from core.exceptions.custom_exception import ConflictException, NotFoundException

UPLOAD_DIR = "uploads"


class StudentService:
    """Business logic layer for managing students."""

    def __init__(self, repository: StudentRepository):
        """Initialize service with student repository."""
        self.repository = repository

    # ---------------- CREATE ----------------

    def create_students(self, data: list[StudentCreate]):
        """Create multiple students after checking for duplicate emails."""
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
        """Return all active students."""
        return self.repository.get_all_active()

    def get_student(self, student_id: int):
        """Retrieve a student by ID."""
        student = self.repository.get_by_id(student_id)

        if not student:
            raise NotFoundException("Student not found")

        return student

    # ---------------- UPDATE ----------------

    def update_students(self, data: list[StudentUpdate]):
        """Update multiple student records."""
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
        """Soft delete students by marking them inactive."""
        students = self.repository.get_by_ids(ids)

        if not students:
            raise NotFoundException("Student not found")

        for student in students:
            student.is_active = False

        self.repository.update_many(students)

    # ---------------- SAVE FILE NAME ----------------

    def save_uploaded_file(self, student_id: int, file_name: str):
        """Save uploaded file name and update student processing status."""
        student = self.repository.get_by_id(student_id)

        if not student:
            raise NotFoundException("Student not found")

        student.file_name = file_name
        student.status = "PENDING"

        return self.repository.update_many([student])

    # ---------------- FILE PROCESSING ----------------

    def process_student_file(self, student_id: int):
        """Process uploaded student file in background."""
        student = self.repository.get_by_id(student_id)

        if not student:
            return

        # Start processing
        student.status = "PROCESSING"
        self.repository.update_many([student])

        if not student.file_name:
            student.status = "FAILED"
            student.result = "File not found"
            self.repository.update_many([student])
            return

        file_path = os.path.join(UPLOAD_DIR, student.file_name)

        # Check if file exists
        if not os.path.exists(file_path):
            student.status = "FAILED"
            student.result = "File not found"
            self.repository.update_many([student])
            return

        try:
            with open(file_path, "rb") as file:
                file.read()

            student.status = "COMPLETED"
            student.result = "Processing completed"

        except OSError as exc:
            student.status = "FAILED"
            student.result = str(exc)

        self.repository.update_many([student])
