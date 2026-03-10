from sqlalchemy import Column, Integer, String
from app.core.database import Base


class File(Base):
    """
    Database model for uploaded files.
    """

    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    status = Column(String)
    