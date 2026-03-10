"""
student_schema.py

This module defines Pydantic schemas for Student objects used in API requests
and responses. Schemas ensure proper validation of input data and structured
output in API responses.
"""

from pydantic import BaseModel


class StudentCreate(BaseModel):  # pylint: disable=too-few-public-methods
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

    def __repr__(self) -> str:
        """Return string representation of StudentCreate."""
        return f"StudentCreate(name={self.name!r}, age={self.age}, marks={self.marks})"


class StudentUpdate(BaseModel):  # pylint: disable=too-few-public-methods
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

    def __repr__(self) -> str:
        """Return string representation of StudentUpdate."""
        return f"StudentUpdate(name={self.name!r}, age={self.age}, marks={self.marks})"


class StudentResponse(BaseModel):  # pylint: disable=too-few-public-methods
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

    class Config:  # pylint: disable=too-few-public-methods
        """
        Pydantic model configuration.

        Attributes:
            from_attributes (bool): Allows population of this schema from ORM model attributes.
        """

        from_attributes = True

    def __repr__(self) -> str:
        """Return string representation of StudentResponse."""
        return (
            f"StudentResponse(id={self.id}, name={self.name!r}, "
            f"age={self.age}, marks={self.marks})"
        )
