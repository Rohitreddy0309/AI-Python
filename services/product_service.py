from sqlalchemy.orm import Session
from repositories.product_repository import ProductRepository
from utils.exceptions import NotFoundException

class ProductService:

    @staticmethod
    def get_all_products(db: Session):
        return ProductRepository.get_all(db)

    @staticmethod
    def get_product(db: Session, product_id: int):
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise NotFoundException("Product not found")
        return product

    @staticmethod
    def create_product(db: Session, product_data: dict):
        return ProductRepository.create(db, product_data)

    @staticmethod
    def update_product(db: Session, product_id: int, product_data: dict):
        db_product = ProductRepository.get_by_id(db, product_id)
        if not db_product:
            raise NotFoundException("Product not found")
        return ProductRepository.update(db, db_product, product_data)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = ProductRepository.get_by_id(db, product_id)
        if not db_product:
            raise NotFoundException("Product not found")
        ProductRepository.delete(db, db_product)