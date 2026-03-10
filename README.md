# Product CRUD API

A backend REST API built using **FastAPI** that demonstrates production-style backend architecture including CRUD operations, middleware, background tasks, rate limiting, dependency injection, exception handling, environment configuration, and automated testing.

# Features

- Product CRUD operations
- Bulk Create / Update / Delete APIs
- File upload with background processing
- Request logging middleware
- Rate limiting (per IP)
- Custom exception handling
- Dependency Injection pattern
- Service–Repository architecture
- Environment configuration using `.env`
- Automated testing with Pytest
- Code quality standardization using pylint


# Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn
- Pytest
- Passlib (bcrypt)
- aiofiles
- python-dotenv

# Environment Configuration

Environment variables are stored in `.env`.

Example:

DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/postgres
APP_NAME=Product CRUD API
DEBUG=True


# Installation

Clone the repository:


git clone <your-repo-url>
cd Product_CRUD


Create virtual environment:


python -m venv venv


Activate virtual environment

Windows:


venv\Scripts\activate


Install dependencies:


pip install -r requirements.txt


# Run the Application

Start the FastAPI server:


uvicorn main:app --reload


API will run at:


http://127.0.0.1:8000


Swagger documentation:


http://127.0.0.1:8000/docs



# Running Tests

Run pytest:


pytest


Run with coverage:


pytest --cov=.


# Rate Limiting

Rate limiting is implemented using an in-memory request store.

Limit:


10 requests per minute per IP


# Code Quality

Code quality is maintained using **pylint**.

Run linting:


pylint .


# Author

Akshay Reddy
