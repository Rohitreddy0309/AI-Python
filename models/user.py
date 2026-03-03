from sqlalchemy import Column, Integer, String, Boolean,DateTime
from sqlalchemy.sql import func
from core.database import base

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    department = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
)
    photo = Column(String, nullable=True)