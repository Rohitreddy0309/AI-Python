"""
Repository layer for user-related database operations.

This module contains functions that interact directly with the database
to perform CRUD operations for the User model.
"""

from sqlalchemy.orm import Session

from models.user import User


def get_all_users(db: Session):
    """
    Retrieve all users from the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        list[User]: List of all user records.
    """
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a user by their ID.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user.

    Returns:
        User | None: The user if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email address.

    Args:
        db (Session): SQLAlchemy database session.
        email (str): Email of the user.

    Returns:
        User | None: The user if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User):
    """
    Create a new user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (User): User object to be created.

    Returns:
        User: The created user record.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User):
    """
    Update an existing user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (User): User object with updated fields.

    Returns:
        User: The updated user record.
    """
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    """
    Delete a user from the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (User): User object to be deleted.
    """
    db.delete(user)
    db.commit()


def bulk_create(db: Session, users: list[User]):
    """
    Create multiple users in the database at once.

    Args:
        db (Session): SQLAlchemy database session.
        users (list[User]): List of User objects to be created.

    Returns:
        list[User]: List of created user records.
    """
    db.add_all(users)
    db.commit()

    for user in users:
        db.refresh(user)
    return users
