from fastapi import FastAPI
from api import emp_routes, task_routes
from utils.exceptions import app_exception_handler, generic_exception_handler,AppException
app = FastAPI(title="Employee & Task Management API")


app.include_router(emp_routes.router)
app.include_router(task_routes.router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
def root():
    return {"message": "Welcome to the Employee & Task Management API"}