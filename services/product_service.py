"""
Product service layer.

This module contains business logic related to product operations.
It acts as an intermediary between the API routes and the repository
layer, ensuring validation and workflow rules are applied.
"""

import asyncio

from core.database import SessionLocal
from repositories.product_repository import ProductRepository
from schemas.product import ProductBulkUpdate, ProductCreate
from utils.exceptions import NotFoundException, WorkflowTransitionException


class ProductService:
    """
    Service layer responsible for product business logic.
    """

    def __init__(self, db):
        """
        Initialize the ProductService with a database session.
        """
        self.db = db

    def get_all_products(self):
        """Retrieve all products."""
        return ProductRepository.get_all(self.db)

    def get_product(self, product_id: int):
        """Retrieve a product by ID."""
        product = ProductRepository.get_by_id(self.db, product_id)
        if not product:
            raise NotFoundException("Product not found")
        return product

    def create_product(self, product_data: dict):
        """Create a new product."""
        return ProductRepository.create(self.db, product_data)

    def update_product(self, product_id: int, product_data: dict):
        """Update an existing product."""
        db_product = ProductRepository.get_by_id(self.db, product_id)

        if not db_product:
            raise NotFoundException("Product not found")

        return ProductRepository.update(self.db, db_product, product_data)

    def delete_product(self, product_id: int):
        """Delete a product."""
        db_product = ProductRepository.get_by_id(self.db, product_id)

        if not db_product:
            raise NotFoundException("Product not found")

        ProductRepository.delete(self.db, db_product)

    def bulk_create_products(self, products: list[ProductCreate]):
        """Create multiple products."""

        if len(products) > 1000:
            raise WorkflowTransitionException(
                status_code=400,
                message="Maximum 1000 records allowed"
)

        product_dicts = [product.model_dump() for product in products]

        return ProductRepository.bulk_create(self.db, product_dicts)

    def get_products_by_ids(self, ids: list[int]):
        """Retrieve multiple products by their IDs."""
        products = ProductRepository.get_by_ids(self.db, ids)

        if not products:
            raise NotFoundException("Product not found")

        return products

    def bulk_update_products(self, products: list[ProductBulkUpdate]):
        """Update multiple products."""
        product_dicts = [product.model_dump() for product in products]

        return ProductRepository.bulk_update(self.db, product_dicts)

    def bulk_delete_products(self, ids: list[int]):
        """Delete multiple products."""
        return ProductRepository.bulk_delete(self.db, ids)

    @staticmethod
    async def process_product_file(product_id: int):
        """
        Background task to simulate file processing.

        Updates product file status during processing.
        """

        db = SessionLocal()

        try:
            ProductRepository.update_file_status(db, product_id, "PROCESSING")

            await asyncio.sleep(5)  # Simulates file parsing

            result = "File parsed successfully"

            ProductRepository.update_file_status(
                db,
                product_id,
                "COMPLETED",
                result
            )

        finally:
            db.close()
