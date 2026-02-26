from fastapi import FastAPI
from api.v1.router import router
from utils.handlers import register_exception_handlers

app = FastAPI()
app.include_router(router)

register_exception_handlers(app)
