from fastapi import FastAPI

from core.database import engine, Base
from api.v1.router import api_router

from middleware.request_logger import RequestLoggingMiddleware
from models import request_log

from utils.exception_handlers import base_exception_handler
from utils.exceptions import BaseAppException


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(RequestLoggingMiddleware)

app.add_exception_handler(BaseAppException, base_exception_handler)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "CRUD API is running "}