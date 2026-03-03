from sqlalchemy.orm import Session
from repositories.product_repository import ProductRepository
from utils.exceptions import NotFoundException
from schemas.product import ProductCreate
from fastapi import HTTPException
from schemas.product import ProductBulkUpdate
import asyncio
from core.database import SessionLocal

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



    @staticmethod
    def bulk_create_products(db: Session, products: list[ProductCreate]):

        if len(products) > 1000:
            raise HTTPException(status_code=400, detail="max 1000 records allowed")
        
        product_dicts = [product.model_dump() for product in products]
        return ProductRepository.bulk_create(db, product_dicts)
        
    @staticmethod
    def get_products_by_ids(db: Session, ids: list[int]):
        products = ProductRepository.get_by_ids(db, ids)
        if not products:
            raise NotFoundException("Product not Found")
        return products
    
    @staticmethod
    def bulk_update_products(db: Session, products: list[ProductBulkUpdate]):
        product_dicts = [product.model_dump() for product in products]
        return ProductRepository.bulk_update(db, product_dicts)
    
    @staticmethod
    def bulk_delete_products(db: Session, ids: list[int]):
        return ProductRepository.bulk_delete(db, ids)
    

    @staticmethod
    async def process_product_file(product_id: int):
        db = SessionLocal()

        try:
            ProductRepository.update_file_status(db, product_id, "PROCESSING")

            await asyncio.sleep(5)  #It simulates parsing

            result = "File parsed successfully"

            ProductRepository.update_file_status(
                db,
                product_id,
                "COMPLETED",
                result
            )
        finally:
            db.close()


    

