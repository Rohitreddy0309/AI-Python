"""
student_service.py

This module defines the StudentService class, which acts as a business logic layer
for managing student data. It interacts with the StudentRepository to perform
CRUD operations and handles exceptions such as not found errors.
"""

from sqlalchemy.orm import Session

from app.repositories.student_repository import StudentRepository
from fastapi import HTTPException


class StudentService:
    """
    Service class for performing business logic related to Student operations.

    Attributes:
        repository (StudentRepository): Instance of StudentRepository used for database operations.
    """

    def __init__(self):
        """
        Initialize the StudentService with a StudentRepository instance.
        """
        self.repository = StudentRepository()

    def create_student(self, db: Session, name: str, age: int, marks: int):
        """
        Create a new student record.

        Args:
            db (Session): SQLAlchemy database session.
            name (str): Name of the student.
            age (int): Age of the student.
            marks (int): Marks of the student.

        Returns:
            Student: The newly created Student object.
        """
        return self.repository.create_student(db, name, age, marks)

    def get_students(self, db: Session):
        """
        Retrieve all students from the database.

        Args:
            db (Session): SQLAlchemy database session.

        Returns:
            list[Student]: List of all Student objects.
        """
        return self.repository.get_all_students(db)

    def get_student(self, db: Session, student_id: int):
        """
        Retrieve a single student by ID, raising an exception if not found.

        Args:
            db (Session): SQLAlchemy database session.
            student_id (int): ID of the student to retrieve.

        Raises:
            HTTPException: If the student is not found (404).

        Returns:
            Student: The requested Student object.
        """
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    def get_student_by_id(self, db: Session, student_id: int):
        """
        Retrieve a student by ID (alternate method), raising an exception if not found.

        Args:
            db (Session): SQLAlchemy database session.
            student_id (int): ID of the student to retrieve.

        Raises:
            HTTPException: If the student is not found (404).

        Returns:
            Student: The requested Student object.
        """
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    def update_student(
        self, db: Session, student_id: int, name: str, age: int, marks: int
    ):
        """
        Update an existing student's information.

        Args:
            db (Session): SQLAlchemy database session.
            student_id (int): ID of the student to update.
            name (str): Updated name of the student.
            age (int): Updated age of the student.
            marks (int): Updated marks of the student.

        Raises:
            HTTPException: If the student is not found (404).

        Returns:
            Student: The updated Student object.
        """
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return self.repository.update_student(db, student, name, age, marks)

    def delete_student(self, db: Session, student_id: int):
        """
        Delete a student record from the database.

        Args:
            db (Session): SQLAlchemy database session.
            student_id (int): ID of the student to delete.

        Raises:
            HTTPException: If the student is not found (404).

        Returns:
            dict: Confirmation message after successful deletion.
        """
        student = self.repository.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        self.repository.delete_student(db, student)
        return {"message": "Student deleted successfully"}
