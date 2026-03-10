"""
Student database model.

Represents student records stored in the database.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Student(Base):  # pylint: disable=too-few-public-methods
    """
    SQLAlchemy model for the 'students' table.

    Attributes:
        id (int): Student ID
        name (str): Student name
        age (int): Student age
        marks (int): Student marks
    """

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    marks = Column(Integer)

    def __repr__(self) -> str:
        """Return string representation of Student."""
        return f"Student(id={self.id}, name={self.name!r}, age={self.age}, marks={self.marks})"
