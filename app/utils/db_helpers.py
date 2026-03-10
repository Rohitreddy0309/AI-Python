"""
Database helper functions.

This module contains utility functions for common database operations.
"""

from sqlalchemy.orm import Session


def get_lowest_available_id(db: Session, model):
    """
    Find the lowest available ID not currently in use in the database.

    Args:
        db (Session): SQLAlchemy database session.
        model: SQLAlchemy model class with an id column.

    Returns:
        int: Lowest available ID.
    """
    ids = db.query(model.id).order_by(model.id).all()

    expected = 1
    for (id_val,) in ids:
        if id_val != expected:
            return expected
        expected += 1

    return expected
