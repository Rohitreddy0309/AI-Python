"""
request_log_repository.py

This module defines the RequestLogRepository class which provides
methods to interact with the RequestLog model in the database.
It allows creating log entries for HTTP requests including metadata
such as request ID, HTTP method, endpoint, client IP, and response time.
"""

from sqlalchemy.orm import Session

from app.models.request_log import RequestLog


class RequestLogRepository:  # pylint: disable=too-few-public-methods
    """
    Repository class for interacting with RequestLog records in the database.

    Methods:
        create_log(db, request_id, method, endpoint, ip_address, response_time):
            Creates a new request log entry.
    """

    def __repr__(self) -> str:
        """Return string representation of RequestLogRepository."""
        return "RequestLogRepository()"

    def create_log(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        db: Session,
        request_id: str,
        method: str,
        endpoint: str,
        ip_address: str,
        response_time: float,
    ):
        """
        Create a new request log entry in the database.

        Args:
            db (Session): SQLAlchemy database session.
            request_id (str): Unique identifier for the request.
            method (str): HTTP method of the request (GET, POST, etc.).
            endpoint (str): URL path accessed by the request.
            ip_address (str): IP address of the client making the request.
            response_time (float): Time taken to process the request (in seconds).

        Returns:
            None
        """
        log = RequestLog(
            request_id=request_id,
            method=method,
            endpoint=endpoint,
            ip_address=ip_address,
            response_time=response_time,
        )

        db.add(log)
        db.commit()
