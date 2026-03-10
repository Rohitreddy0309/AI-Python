"""ORM model representing a task."""

from sqlalchemy import Boolean, Column, Integer, String

from core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    # Optional file attached to the task
    file_name = Column(String, nullable=True)
