"""
Repository functions for handling request log records in the database.
"""

from sqlalchemy.orm import Session

from models.request_logs import RequestLog


def create_log(db: Session, log_data: dict):
    """
    Create and store a request log entry in the database.

    Args:
        db (Session): Active SQLAlchemy database session.
        log_data (dict): Dictionary containing request log details.

    Returns:
        RequestLog: The created request log record.
    """

    log = RequestLog(**log_data)

    db.add(log)
    db.commit()
    db.refresh(log)
    return log
