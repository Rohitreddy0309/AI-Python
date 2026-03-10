# Employee & Task Management API

A simple FastAPI-based REST API for managing employees and tasks, including file uploads and request logging.

## 🚀 Features

- CRUD operations for **Employees** and **Tasks**
- File upload support for tasks (stored under `uploads/`)
- Request logging persisted to the database
- Structured error handling with custom exception responses
- Pydantic schemas for input validation and response models

## 🧩 Project Structure

- `main.py` — FastAPI application entry point
- `api/` — Routers defining API endpoints
- `service/` — Business logic layer (services)
- `repository/` — Database access layer (SQLAlchemy)
- `schemas/` — Pydantic request/response models
- `models/` — SQLAlchemy ORM models
- `dependencies/` — Dependency providers (FastAPI DI)
- `middleware/` — Custom middleware (request logging)
- `core/` — App configuration, database setup, logging
- `utils/` — Utility modules and custom exception handling

## ✅ Requirements

- Python 3.11+
- Virtual environment recommended

## ⚙️ Setup

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file at the project root with at least the database URL:

```
DATABASE_URL=sqlite:///./app.db
```

## ▶️ Running the App

```powershell
uvicorn main:app --reload
```

Then open: `http://127.0.0.1:8000`

API docs are available at:
- OpenAPI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🧪 Tests

Run tests with:

```powershell
pytest
```

## 🧠 Notes

- Database tables are created automatically at startup via `Base.metadata.create_all(bind=engine)`.
- Request logs are stored in the `request_logs` table.
- Uploaded files are stored in the `uploads/` directory.

## 🗂️ Endpoints (Summary)

### Employees
- `GET /employees/` — list employees
- `POST /employees/` — create employee
- `PUT /employees/{emp_id}` — update employee
- `DELETE /employees/{emp_id}` — delete employee

### Tasks
- `GET /tasks/` — list tasks
- `POST /tasks/` — create task
- `PUT /tasks/{task_id}` — update task
- `DELETE /tasks/{task_id}` — delete task
- `POST /tasks/{task_id}/upload` — upload file for task

---


