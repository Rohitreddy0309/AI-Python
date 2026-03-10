# Student CRUD API

A **FastAPI backend application** for managing student records.

The API supports **CRUD operations, file uploads, background processing, rate limiting, middleware logging, custom exception handling, and dependency injection**.

This project demonstrates a **production-style backend design** with **middleware logging, rate limiting, background tasks, and a clean layered architecture (Router → Service → Repository)** using **PostgreSQL** as the database.

---

##  Features

* Create, Read, Update, Delete (CRUD) student records
* File upload with background processing
* Request logging middleware
* Rate limiting to protect APIs
* Custom exception handling
* Dependency injection
* Environment configuration using `.env`
* Auto-generated API documentation

---

##  Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Uvicorn
* Pytest

---

##  Project Structure

```
student-crud-api/
│
├── api/
├── core/
├── middleware/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
├── tests/
├── uploads/
│
├── main.py
├── requirements.txt
└── README.md
```

---

##  Installation

Clone the repository

```
git clone <repository-url>
cd student-crud-api
```

Create a virtual environment

```
python -m venv venv
```

Activate the environment

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

---

##  Database Configuration

Create a `.env` file in the root directory.

Example:

```
DATABASE_URL=postgresql://username:password@localhost:5432/student_db
```

---

##  Run the Application

```
uvicorn main:app --reload
```

Server runs at

```
http://127.0.0.1:8000
```

---

##  API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

##  Running Tests

```
pytest
```

---

##  Author

Rohit Reddy

