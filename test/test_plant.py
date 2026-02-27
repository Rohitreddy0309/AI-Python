from fastapi.testclient import TestClient
from test import app

client = TestClient(app)


def test_create_plant():
    response = client.post(
        "/api/v1/plants",
        json={
            "name": "Test Plant",
            "watering_interval_days": 5,
            "sunlight": "Partial Sun",
            "last_watered": "2026-02-20"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Plant"
    assert data["watering_interval_days"] == 5


def test_get_all_plants():
    response = client.get("/api/v1/plants")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_invalid_plant():
    response = client.get("/api/v1/plants/999999")
    assert response.status_code == 404


def test_update_plant():
    # First create
    create_response = client.post(
        "/api/v1/plants",
        json={
            "name": "Update Test",
            "watering_interval_days": 7,
            "sunlight": "Full Sun",
            "last_watered": "2026-02-21"
        }
    )
    plant_id = create_response.json()["id"]

    # Update
    update_response = client.put(
        f"/api/v1/plants/{plant_id}",
        json={
            "name": "Updated Name",
            "watering_interval_days": 10,
            "sunlight": "Full Sun",
            "last_watered": "2026-02-22"
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Name"


def test_delete_plant():
    # Create plant first
    create_response = client.post(
        "/api/v1/plants",
        json={
            "name": "Delete Test",
            "watering_interval_days": 3,
            "sunlight": "Low Light",
            "last_watered": "2026-02-19"
        }
    )
    plant_id = create_response.json()["id"]

    # Delete
    delete_response = client.delete(f"/api/v1/plants/{plant_id}")
    assert delete_response.status_code == 200

    # Confirm deletion
    get_response = client.get(f"/api/v1/plants/{plant_id}")
    assert get_response.status_code == 404
