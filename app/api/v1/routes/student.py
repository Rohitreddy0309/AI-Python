"""
Student API Routes.

Provides endpoints for creating, retrieving,
updating, and deleting students.
"""

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.student_service import StudentService
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/students", tags=["Students"])

student_service = StudentService()


@router.post("/")
def create_student(name: str, age: int, marks: int, db: Session = Depends(get_db)):
    """
    Create a new student.

    Args:
        name (str): Student name
        age (int): Student age
        marks (int): Student marks
        db (Session): Database session

    Returns:
        Student: Created student record
    """
    return student_service.create_student(db, name, age, marks)


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    """
    Retrieve all students.

    Args:
        db (Session): Database session

    Returns:
        List[Student]: List of students
    """
    return student_service.get_students(db)


@router.get("/{student_id}")
def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a student by their ID.

    Args:
        student_id (int): ID of the student
        db (Session): Database session

    Returns:
        Student: The requested student record
    """
    return student_service.get_student_by_id(db, student_id)


@router.put("/{student_id}")
def update_student(
    student_id: int, name: str, age: int, marks: int, db: Session = Depends(get_db)
):
    """
    Update a student's information.

    Args:
        student_id (int): ID of the student
        name (str): Updated student name
        age (int): Updated student age
        marks (int): Updated student marks
        db (Session): Database session

    Returns:
        Student: The updated student record
    """
    return student_service.update_student(db, student_id, name, age, marks)


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Delete a student by their ID.

    Args:
        student_id (int): ID of the student
        db (Session): Database session

    Returns:
        dict: Confirmation message
    """
    return student_service.delete_student(db, student_id)
