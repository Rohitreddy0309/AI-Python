"""
Product schema definitions.

This module contains Pydantic models used for request validation
and response serialization in the Product API.
"""

# pylint: disable=too-few-public-methods

from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    """
    Base schema containing common product fields.
    """

    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    """
    Schema used for creating a new product.
    """


class ProductResponse(ProductBase):
    """
    Schema used for returning product data in API responses.
    """

    id: int
    file_name: Optional[str] = None
    file_status: Optional[str] = None
    file_result: Optional[str] = None

    class Config:
        """
        Enables compatibility with ORM objects.
        """

        from_attributes = True


class ProductBulkUpdate(ProductBase):
    """
    Schema used for updating multiple products.
    """

    id: int
