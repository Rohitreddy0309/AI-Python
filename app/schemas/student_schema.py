"""
student_schema.py

This module defines Pydantic schemas for Student objects used in API requests
and responses. Schemas ensure proper validation of input data and structured
output in API responses.
"""

from pydantic import BaseModel


class StudentCreate(BaseModel):
    """
    Schema for creating a new student.

    Attributes:
        name (str): Name of the student.
        age (int): Age of the student.
        marks (int): Marks obtained by the student.
    """

    name: str
    age: int
    marks: int


class StudentUpdate(BaseModel):
    """
    Schema for updating an existing student.

    Attributes:
        name (str): Updated name of the student.
        age (int): Updated age of the student.
        marks (int): Updated marks of the student.
    """

    name: str
    age: int
    marks: int


class StudentResponse(BaseModel):
    """
    Schema for returning student information in API responses.

    Attributes:
        id (int): Unique identifier of the student.
        name (str): Name of the student.
        age (int): Age of the student.
        marks (int): Marks obtained by the student.
    """

    id: int
    name: str
    age: int
    marks: int

    class Config:
        """
        Pydantic model configuration.

        Attributes:
            from_attributes (bool): Allows population of this schema from ORM model attributes.
        """

        from_attributes = True
