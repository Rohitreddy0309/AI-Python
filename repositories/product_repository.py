from sqlalchemy.orm import Session
from models.product import Product

class ProductRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def create(db: Session, product_data: dict):
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(db: Session, db_product, product_data: dict):
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, db_product):
        db.delete(db_product)
        db.commit()


    @staticmethod
    def bulk_create(db: Session, products_data: list[dict]):
        products = [Product(**data) for data in products_data]

        db.add_all(products)
        db.commit()

        for product in products:
            db.refresh(product)

        return products
    
    @staticmethod
    def get_by_ids(db: Session, ids: list[list]):
        return db.query(Product).filter(Product.id.in_(ids)).all()

    @staticmethod
    def bulk_update(db: Session, products_data: list[dict]):
        updated_products = []

        for data in products_data:
            product = db.query(Product).filter(Product.id == data["id"]).first()

            if product:
                for key, value in data.items():
                    if key != "id":
                        setattr(product, key, value)
                        
                updated_products.append(product)

        db.commit()

        for product in updated_products:
            db.refresh(product)

        return updated_products
    
    @staticmethod
    def bulk_delete(db: Session, ids: list[int]):
        products = db.query(Product).filter(Product.id.in_(ids)).all()

        for product in products:
            db.delete(product)

        db.commit()

        return {"deleted_count": len(products)}
    
    @staticmethod
    def update_file_info(db: Session, product_id: int, file_name: str, file_path: str):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.file_name = file_name
            product.file_path = file_path
            product.file_status = "PENDING"
            db.commit()
            db.refresh(product)
        return product
    
    @staticmethod
    def update_file_status(db: Session, product_id: int, status: str, result: str | None = None):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.file_status = status
            if result:
                product.file_result = result
            db.commit()
            db.refresh(product)
        return product
    

    
        
