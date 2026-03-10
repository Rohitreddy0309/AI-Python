#performing fast api using crud operations
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from model1 import product
from database1 import Base, Sessionlocal, engine, get_db
import database_model1

app=FastAPI()

database_model1.Base.metadata.create_all(bind=engine)
products = [
    product(id=1,name="tata",description="nexon",price=1000,quantity=10),
    product(id=2,name="mahindra",description="scoripo",price=2000,quantity=20),
    product(id=3,name="hundai",description="creta",price=3000,quantity=30),
    product(id=4,name="maruti",description="swift",price=4000,quantity=40),
    product(id=5,name="toyata",description="innova",price=5000,quantity=50),
    product(id=6,name="kia",description="carnes",price=6000,quantity=60),
    ]


def init_db():
    db=Session()

    count = db.query(database_model1.product).count
    if count == 0:
        for product in products:
            db.add(database_model1.product(**product.model_dump()))
        db.commit()
init_db()


@app.get("/products/{id}")
def product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_model1.product).filter(database_model1.product.id == id).first()
    if db_product:
        return db_product
    return "no product found"

@app.get("/product")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model1.product).all()
    
    #db.query()
    return db_products

@app.put("/product")
def update_product(id:int, product:product, db: Session = Depends(get_db)):
    db_product = db.query(database_model1.product).filter(database_model1.product.id == id).first()
    if db_product:
        db_product.name= product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "product updated"
    else:
        return "no product found"

@app.post("/product")
def add_product(product:product, db: Session = Depends(get_db)):
    db.add(database_model1.product(**product.model_dump()))
    db.commit()
    return product

@app.delete("/product")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_model1.product).filter(database_model1.product.id == id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return "deleted successfully"
    else:
        return "no product found"

