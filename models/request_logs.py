"""
SQLAlchemy model for storing API request logs.

This model captures details about incoming API requests such as
endpoint accessed, response status, response time, and the client
IP address. It is mainly used for monitoring, debugging, and
tracking request behavior in the application.
"""

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from core.database import base


class RequestLog(base):
    """
    Database model representing a request log entry.

    Each record stores metadata about an API request including
    request identifier, endpoint accessed, response status,
    response time, and the originating IP address.
    """

    __tablename__ = "request_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(String, nullable=True)

    request_id = Column(String)
    endpoint = Column(String)
    ip_address = Column(String)

    status_code = Column(Integer)
    status_message = Column(String)

    response_time = Column(Float)

    created_at = Column(DateTime, server_default=func.now())
