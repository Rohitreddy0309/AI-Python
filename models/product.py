"""
Product database model.

This module defines the SQLAlchemy Product model which represents
the products table in the database. It stores product details
along with optional file processing information.
"""

# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Float, Integer, String, Text

from core.database import Base


class Product(Base):
    """
    SQLAlchemy model representing a product.

    Fields:
    - id: Primary key
    - name: Product name
    - description: Product description
    - price: Product price
    - quantity: Available quantity
    - file_name: Uploaded file name
    - file_path: Location of uploaded file
    - file_status: Processing status of the file
    - file_result: Result of background file processing
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    file_status = Column(String, default="PENDING")
    file_result = Column(Text, nullable=True)
