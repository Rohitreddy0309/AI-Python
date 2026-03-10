import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_employees():
    response = client.get("/employees/")
    assert response.status_code in [200, 404]


def test_create_employee():
    payload = {
        "name": "Test Employee",
        "email": "test@example.com",
    }

    response = client.post("/employees/", json=payload)

    assert response.status_code in [200, 201]


def test_update_employee():
    payload = {
        "name": "Updated Employee",
        "email": "updated@example.com",
    }

    response = client.put("/employees/1", json=payload)

    assert response.status_code in [200, 404]


def test_delete_employee():
    response = client.delete("/employees/1")

    assert response.status_code in [200, 404]
