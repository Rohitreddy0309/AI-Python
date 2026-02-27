from fastapi import FastAPI
from api.v1.router import api_router
from core.database import Base, engine


# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI instance (must be global)
app = FastAPI(title="Student CRUD API")

@app.get("/")
def root():
    return {"message": "Student CRUD API is running "}
# Include API routes
app.include_router(api_router, prefix="/api/v1")