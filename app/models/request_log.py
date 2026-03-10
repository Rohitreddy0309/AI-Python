"""
request_log.py

This module defines the RequestLog model for storing HTTP request logs
in the database using SQLAlchemy ORM. Each log entry records metadata
about a request including its unique ID, endpoint, HTTP method, client IP,
response time, and optional associated file or student information.
"""

from sqlalchemy import Column, Float, Integer, String

from app.core.database import Base


class RequestLog(Base):  # pylint: disable=too-few-public-methods
    """
    SQLAlchemy model representing a log of an HTTP request.

    Attributes:
        id (int): Primary key of the log entry.
        request_id (str): Unique identifier for the request.
        method (str): HTTP method (GET, POST, etc.).
        endpoint (str): URL path of the request.
        ip_address (str): Client IP address that made the request.
        response_time (float): Time taken to process the request (in seconds).
        filename (str, optional): Name of an associated file, if any.
        student_name (str, optional): Name of a student included in the request body, if any.
    """

    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True)
    method = Column(String)
    endpoint = Column(String)
    ip_address = Column(String)
    response_time = Column(Float)
    filename = Column(String, nullable=True)
    student_name = Column(String, nullable=True)

    def __repr__(self) -> str:
        """Return string representation of RequestLog."""
        return (
            f"RequestLog(id={self.id}, request_id={self.request_id!r}, "
            f"method={self.method!r}, endpoint={self.endpoint!r}, "
            f"response_time={self.response_time})"
        )
