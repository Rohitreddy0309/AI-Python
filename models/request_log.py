"""
Request log model.

Defines the database table used to store API request logs.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from core.database import Base


class RequestLog(Base):  # pylint: disable=too-few-public-methods
    """SQLAlchemy model for storing API request logs."""

    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String, index=True)

    ip_address = Column(String)

    path = Column(String)

    status_code = Column(String)

    response_time = Column(Float)

    created_at = Column(DateTime, server_default=func.now())  # pylint: disable=not-callable
