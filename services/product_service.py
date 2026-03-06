from sqlalchemy.orm import Session
from repositories.product_repository import ProductRepository
from utils.exceptions import NotFoundException
from schemas.product import ProductCreate
from schemas.product import ProductBulkUpdate
import asyncio
from core.database import SessionLocal
from utils.exceptions import WorkflowTransitionException

class ProductService:

    def __init__(self, db):
        self.db = db


    def get_all_products(self):
        return ProductRepository.get_all(self.db)


    def get_product(self, product_id: int):
        product = ProductRepository.get_by_id(self.db, product_id)
        if not product:
            raise NotFoundException("Product not found")
        return product


    def create_product(self, product_data: dict):
        return ProductRepository.create(self.db, product_data)

    
    def update_product(self, product_id: int, product_data: dict):
        db_product = ProductRepository.get_by_id(self.db, product_id)
        if not db_product:
            raise NotFoundException("Product not found")
        return ProductRepository.update(self.db, db_product, product_data)

    
    def delete_product(self, product_id: int):
        db_product = ProductRepository.get_by_id(self.db, product_id)
        if not db_product:
            raise NotFoundException("Product not found")
        ProductRepository.delete(self.db, db_product)



    def bulk_create_products(self, products: list[ProductCreate]):

        if len(products) > 1000:
            raise WorkflowTransitionException("Maximum 1000 records allowed")
        
        product_dicts = [product.model_dump() for product in products]
        return ProductRepository.bulk_create(self.db, product_dicts)
        
    
    def get_products_by_ids(self, ids: list[int]):
        products = ProductRepository.get_by_ids(self.db, ids)
        if not products:
            raise NotFoundException("Product not Found")
        return products
    
    
    def bulk_update_products(self, products: list[ProductBulkUpdate]):
        product_dicts = [product.model_dump() for product in products]
        return ProductRepository.bulk_update(self.db, product_dicts)
    
    
    def bulk_delete_products(self, ids: list[int]):
        return ProductRepository.bulk_delete(self.db, ids)
    

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


    

