# User CRUD API (FastAPI)

A modular **User Management REST API** built with **FastAPI**, **SQLAlchemy**, and **Pydantic**.
This project demonstrates clean backend architecture using **service layer**, **repository pattern**, **middleware**, **rate limiting**, and **file upload handling**.

## Features

* CRUD operations for users
* Profile photo upload
* Bulk create and bulk update
* Background file processing
* Request logging middleware
* Rate limiting
* Custom exception handling
* Environment-based configuration
* Clean layered architecture

## Tech Stack

* **FastAPI**
* **Python**
* **SQLAlchemy**
* **Pydantic**
* **Uvicorn**
* **Aiofiles**
* **SQLite / PostgreSQL**
* **Pydantic Settings**

---

## Project Structure

```
user_crud/
│
├── api/
│   └── v1/
│       └── router.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── request_logger.py
│
├── models/
│   ├── user.py
│   ├── file_data.py
│   └── request_logs.py
│
├── repositories/
│   ├── user_repository.py
│   ├── file_repo.py
│   └── request_log_repo.py
│
├── services/
│   ├── user_service.py
│   └── background_service.py
│
├── utils/
│   ├── exceptions.py
│   ├── baseExceptions.py
│   ├── handlers.py
│   ├── rate_limiter.py
│   └── file_handler.py
│
├── Schemas/
│   └── user.py
│
├── uploads/
│
├── main.py
├── .env
└── README.md
```

---

## API Endpoints

### Users

| Method | Endpoint                         | Description            |
| ------ | -------------------------------- | ---------------------- |
| GET    | `/api/v1/users`                  | Get all users          |
| GET    | `/api/v1/users/get/{user_id}`    | Get user by ID         |
| POST   | `/users/add`                     | Create user with photo |
| PUT    | `/users/update/{user_id}`        | Update user            |
| GET    | `/api/v1/users/delete/{user_id}` | Delete user            |

---

### Bulk Operations

| Method | Endpoint             | Description       |
| ------ | -------------------- | ----------------- |
| POST   | `/api/v1/users/bulk` | Bulk create users |
| PATCH  | `/api/v1/users/bulk` | Bulk update users |

---

## File Upload

Users can upload profile photos.

Example request:

```
POST /users/add
```

Form Data

```
name
email
department
photo
```

Uploaded files are stored in the **uploads/** directory.

---

## Rate Limiting

Limits requests to:

```
10 requests per minute per user
```

If exceeded:

```
HTTP 429 – Rate Limit Exceeded
```

---

## Request Logging

A custom middleware logs:

* Request ID
* Endpoint
* IP Address
* Status code
* Response time

Logs are stored in the **request_logs** table.

---

## Environment Variables

Create a `.env` file in the root directory.

```
db_url=sqlite:///./users.db
UPLOAD_FOLDER=uploads
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/user-crud-fastapi.git
cd user_crud
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate it

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the server

```
uvicorn main:app --reload
```

Server runs at

```
http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive documentation.

Swagger UI

http://127.0.0.1:8000/docs

ReDoc

http://127.0.0.1:8000/redoc
```

---

## Example Response

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering",
  "is_active": true,
  "photo": "http://localhost:8000/uploads/photo.png",
  "created_date": "2026-03-10T10:20:30"
}
```

---

## Concepts Demonstrated

* FastAPI REST API Development
* Dependency Injection
* Service Layer Pattern
* Repository Pattern
* Middleware Implementation
* Background Tasks
* Async File Handling
* Custom Exception Handling
* Environment Configuration

---

## Future Improvements

* JWT Authentication
* Role-based access control
* Redis-based rate limiting
* Docker deployment
* Automated testing with Pytest

---

## Author

**Radhitha S**
B.Tech – Data Science & Artificial Intelligence
