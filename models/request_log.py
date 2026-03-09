"""
Request log database model.

This module defines the SQLAlchemy model used to store
API request logs captured by the logging middleware.
"""

# pylint: disable=too-few-public-methods

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from core.database import Base


class RequestLog(Base):
    """
    SQLAlchemy model representing a request log entry.

    Fields:
    - id: Primary key
    - request_id: Unique identifier for each request
    - path: API endpoint path
    - ip_address: Client IP address
    - status_code: HTTP response status code
    - status: Text description of the status
    - response_time: Time taken to process the request
    - timestamp: Time when the request was logged
    """

    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String, index=True)
    path = Column(String)

    ip_address = Column(String)

    status_code = Column(Integer)
    status = Column(String)

    response_time = Column(Float)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
