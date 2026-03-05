from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from core.database import base

class FileData(base):
    __tablename__ = "files_data"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)

    upload_status = Column(String, default="uploading")
    parsed_result = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())