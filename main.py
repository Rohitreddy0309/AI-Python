from fastapi import FastAPI
from api import emp_routes, task_routes
from fastapi.middleware.cors import CORSMiddleware
from utils.exceptions import app_exception_handler, generic_exception_handler,AppException
import uvicorn

app = FastAPI(title="Employee & Task Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emp_routes.router)
app.include_router(task_routes.router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get("/")
def root():
    return {"message": "Welcome to the Employee & Task Management API"}