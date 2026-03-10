import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code in [200, 404]


def test_create_task():
    payload = {"title": "Test Task", "description": "pytest task", "completed": False}

    response = client.post("/tasks/", json=payload)

    assert response.status_code in [200, 201]

    data = response.json()
    assert data["title"] == payload["title"]


def test_update_task():
    payload = {
        "title": "Updated Task",
        "description": "updated description",
        "completed": True,
    }

    response = client.put("/tasks/1", json=payload)

    assert response.status_code in [200, 404]


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code in [200, 404]


def test_upload_file():
    files = {"file": ("test.txt", b"hello world")}

    response = client.post("/tasks/1/upload", files=files)

    assert response.status_code in [200, 404]
