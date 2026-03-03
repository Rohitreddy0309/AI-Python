from fastapi import FastAPI
from api.v1.router import router
from utils.handlers import register_exception_handlers
from fastapi.staticfiles import StaticFiles
from core.database import base ,engine
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
base.metadata.create_all(bind=engine)
app.include_router(router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
register_exception_handlers(app)


