from sqlalchemy import Column, Integer, String
from database import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    status = Column(String)  # processing / completed