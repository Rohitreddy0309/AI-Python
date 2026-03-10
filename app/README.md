# FastAPI Student & File Management API

A FastAPI backend application that manages students and file uploads with additional features like rate limiting, request logging, middleware tracking, and background file processing.

This project follows a clean layered architecture (Routes → Services → Repositories → Database) to maintain scalable and production-ready code.

# Key Features

-->Student CRUD Operations
-->File Upload API
-->Background File Processing
-->Request Logging Middleware
-->Response Time Tracking
-->Request ID Generation
-->IP Address Tracking
-->Rate Limiting (per user)
-->Clean Code Architecture
-->Swagger API Documentation

# Tech Stack

| Technology          | Purpose              |
| ------------------- | -------------------- |
| Python              | Programming Language |
| FastAPI             | API Framework        |
| SQLAlchemy          | ORM                  |
| Pydantic            | Data Validation      |
| PostgreSQL / SQLite | Database             |
| Uvicorn             | ASGI Server          |
| Pytest              | Testing              |


# Project Architecture
The project uses a layered architecture.

Client Request
      ↓
API Routes
      ↓
Services (Business Logic)
      ↓
Repositories (DB Queries)
      ↓
Database

Benefits:

-->Clean code separation
-->Easy debugging
-->Scalable architecture
-->Easy to maintain

# Project Structure
FASTAPI

│
├── app
│   ├── api
│   │   └── v1
│   │       └── routes
│   │           ├── file.py
│   │           ├── student.py
│   │           └── router.py
│
│   ├── core
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logging_config.py
│
│   ├── middleware
│   │   └── request_middleware.py
│
│   ├── models
│   │   ├── file.py
│   │   ├── request_log.py
│   │   └── student.py
│
│   ├── repositories
│   │   ├── file_repository.py
│   │   ├── request_log_repository.py
│   │   └── student_repository.py
│
│   ├── schemas
│   │   ├── file.py
│   │   └── student_schema.py
│
│   ├── services
│   │   ├── file_service.py
│   │   └── student_service.py
│
│   ├── utils
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── rate_limiter.py
│
│   └── main.py
│
├── uploads
├── tests
│   └── test_user.py
│
├── requirements.txt
└── README.md

# Installation
1) Clone Repository
   > git clone https://github.com/chethangoundla-pixel/fastapi-project.git
   > cd fastapi-project

2) Create Virtual Environment
   > python -m venv myenv

3) Activate Virtual Environment
   Windows
   > myenv\Scripts\activate

4) Install Dependencies
   > pip install -r requirements.txt
   Run the Application
   > uvicorn app.main:app --reload

    Server will run at:
    http://127.0.0.1:8000

    Swagger Documentation:
    http://127.0.0.1:8000/docs

# API Endpoints
# Student APIs 

| Method | Endpoint       | Description       |
| ------ | -------------- | ----------------- |
| POST   | /students      | Create student    |
| GET    | /students      | Get all students  |
| GET    | /students/{id} | Get student by ID |
| PUT    | /students/{id} | Update student    |
| DELETE | /students/{id} | Delete student    |

# File APIs

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| POST   | /files   | Upload file         |
| GET    | /files   | List uploaded files |
| Delete | /files   | Delete file         |

# Middleware Features

The custom middleware performs:
-->Request logging
-->Response time calculation
-->Unique request ID generation
-->Client IP address tracking
-->Log storage in database

# Request Logging Middleware
The application includes custom middleware that logs API requests.

Logged information includes:
-->Request ID
-->API endpoint
-->HTTP method
-->Client IP address
-->Response time
-->Student name (if present in request)
Logs are stored in the request_logs table.


# Rate Limiting

Custom rate limiter implemented to prevent API abuse.
Example: 10 requests per minute per user
If the limit is exceeded, the API returns: HTTP 429 - Rate limit exceeded

# Database Tables
The application uses the following tables:

| Table        | Purpose                       |
| ------------ | ----------------------------- |
| students     | Stores student details        |
| files        | Stores uploaded file metadata |
| request_logs | Stores API request logs       |


# Testing
Run tests using: pytest

# Future Improvements

-->JWT Authentication
-->Redis Rate Limiting
-->Docker Support
-->CI/CD Pipeline
-->AWS S3 File Storage
-->Role Based Access Control (RBAC)

# AUTHOR 
CHETHAN GOUNDLA
