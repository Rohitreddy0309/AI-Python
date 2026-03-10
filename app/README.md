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

# .env file
DATABASE_URL=postgresql://postgres:Chethan2004@localhost:5432/studentdb
UPLOAD_DIR=app/uploads

# Middleware Features

The custom middleware performs:
-->Request logging
-->Response time calculation
-->Unique request ID generation
-->Client IP address tracking
-->Log storage in database


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
