from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    """
    Database model for Student entity.
    """

    __tablename__ = "Students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    marks = Column(Integer, nullable=False)

