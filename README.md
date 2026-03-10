# Plant Care API
 A REST API built with FastAPI and PostgreSQL for managing plant care data such as watering schedules and sunlight requirements.

# Features

 CRUD operations for plants
 Bulk create, update, and delete
 File upload with background processing
 Request logging middleware
 Rate limiting
 Automated API tests

# Tech Stack
 Python
 FastAPI
 SQLAlchemy
 PostgreSQL
 Pydantic
 Pytest

# Project Structure
 api/
 core/
 middleware/
 models/
 repositories/
 schemas/
 services/
 utils/
 tests/
 main.py

# Installations
 git clone <repository-url>
 cd project
 python -m venv venv
 pip install -r requirements.txt

# Environment Configuration
 Create a .env file in the project root:
 DATABASE_URL=postgresql://username:password@localhost:5432/plant_db
 ENVIRONMENT=dev
 APP_NAME=Plant API
 DEBUG=True
 SECRET_KEY=your_secret_key  

# Run the Application
 uvicorn main:app --reload
 API Docs: http://127.0.0.1:8000/docs

# Run Tests
 pytest

# Code Quality
 black .
 isort .
 pylint .
  