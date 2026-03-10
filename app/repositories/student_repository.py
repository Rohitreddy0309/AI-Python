"""
student_repository.py

This module defines the StudentRepository class which provides CRUD operations
for the Student model using SQLAlchemy sessions. It supports creating, retrieving,
updating, and deleting student records, as well as finding the lowest available
student ID for new entries.
"""

from sqlalchemy.orm import Session

from app.models.student import Student
from app.utils.db_helpers import get_lowest_available_id


class StudentRepository:
    """
    Repository class for interacting with Student records in the database.

    Methods:
        create_student(db, name, age, marks): Creates a new student record.
        get_all_students(db): Retrieves all student records.
        get_student(db, student_id): Retrieves a student record by ID.
        update_student(db, student, name, age, marks): Updates a student record.
        delete_student(db, student): Deletes a student record.
    """

    def __repr__(self) -> str:
        """Return string representation of StudentRepository."""
        return "StudentRepository()"

    def create_student(self, db: Session, name: str, age: int, marks: int):
        """
        Create a new student record in the database.

        Args:
            db (Session): SQLAlchemy database session.
            name (str): Name of the student.
            age (int): Age of the student.
            marks (int): Marks of the student.

        Returns:
            Student: The newly created Student object.
        """
        new_id = get_lowest_available_id(db, Student)
        student = Student(id=new_id, name=name, age=age, marks=marks)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def get_all_students(self, db: Session):
        """
        Retrieve all student records from the database.

        Args:
            db (Session): SQLAlchemy database session.

        Returns:
            list[Student]: List of all Student objects.
        """
        return db.query(Student).all()

    def get_student(self, db: Session, student_id: int):
        """
        Retrieve a student record by its ID.

        Args:
            db (Session): SQLAlchemy database session.
            student_id (int): ID of the student to retrieve.

        Returns:
            Student | None: The Student object if found, else None.
        """
        return db.query(Student).filter(Student.id == student_id).first()

    def update_student(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self, db: Session, student, name: str, age: int, marks: int
    ):
        """
        Update an existing student record in the database.

        Args:
            db (Session): SQLAlchemy database session.
            student (Student): The Student object to update.
            name (str): Updated name of the student.
            age (int): Updated age of the student.
            marks (int): Updated marks of the student.

        Returns:
            Student: The updated Student object.
        """
        student.name = name
        student.age = age
        student.marks = marks
        db.commit()
        db.refresh(student)
        return student

    def delete_student(self, db: Session, student):
        """
        Delete a student record from the database.

        Args:
            db (Session): SQLAlchemy database session.
            student (Student): The Student object to delete.

        Returns:
            None
        """
        db.delete(student)
        db.commit()
