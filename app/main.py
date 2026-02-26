from fastapi import FastAPI

from app.core.database import engine, Base
from app.api.v1.router import api_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "CRUD API is running "}