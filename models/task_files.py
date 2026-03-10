"""ORM model representing a file attached to a task."""

from sqlalchemy import Column, Integer, String

from core.db import Base


class TaskFile(Base):
    __tablename__ = "task_files"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, index=True)
    filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
