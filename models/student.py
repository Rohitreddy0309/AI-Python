from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from core.database import Base  

class Student(Base):
    """Student database model."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())