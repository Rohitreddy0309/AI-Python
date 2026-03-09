"""
Security utilities for password handling.

This module provides helper functions for hashing passwords
and verifying hashed passwords using the Passlib library.
"""

from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password.

    Args:
        password (str): The plain password provided by the user.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hashed value.

    Args:
        plain_password (str): The password entered by the user.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)
