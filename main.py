from fastapi import FastAPI
from api import emp_routes, task_routes

app = FastAPI(title="Employee & Task Management API")


app.include_router(emp_routes.router)
app.include_router(task_routes.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Employee & Task Management API"}