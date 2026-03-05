from fastapi import FastAPI

from core.database import engine, Base
from api.v1.router import api_router

from middleware.request_logger import RequestLoggingMiddleware
from models import request_log

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "CRUD API is running "}