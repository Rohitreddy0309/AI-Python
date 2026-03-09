"""
Request log repository layer.

This module contains database operations related to request logging.
It provides helper methods to store API request log information
captured by the logging middleware.
"""

# pylint: disable=too-few-public-methods

from sqlalchemy.orm import Session

from models.request_log import RequestLog


class RequestLogRepository:
    """
    Repository class responsible for database interactions
    related to request logs.
    """

    @staticmethod
    def create_log(db: Session, log_data: dict):
        """
        Store a request log entry in the database.

        Args:
            db (Session): SQLAlchemy database session.
            log_data (dict): Data containing request log details.

        Returns:
            RequestLog: The created request log object.
        """
        log = RequestLog(**log_data)

        db.add(log)
        db.commit()
        db.refresh(log)


        return log
 