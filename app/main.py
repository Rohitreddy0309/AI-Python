from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.database import Base, engine

from app.middleware.request_middleware import RequestLoggingMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="File Upload API"
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(
    api_router,
    prefix="/api/v1"
)




