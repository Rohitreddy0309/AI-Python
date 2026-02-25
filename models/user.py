from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.sql import func
from core.database import base

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)   # Required field
    email = Column(String, unique=True, nullable=False)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
  