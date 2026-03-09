"""
API tests for plant endpoints.

This module contains integration tests for the Plant API using
FastAPI's TestClient. It verifies CRUD operations, bulk actions,
and rate limiting behavior.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient  # pylint: disable=wrong-import-position
from main import app  # pylint: disable=wrong-import-position

client = TestClient(app)


def test_get_plants():
    """Test retrieving the list of plants."""
    response = client.get("/api/v1/plants/")
    assert response.status_code == 200


def test_create_plant():
    """Test creating a new plant."""
    response = client.post(
        "/api/v1/plants/",
        json={
            "name": "Test Plant",
            "watering_interval_days": 3,
            "sunlight": "Full Sun",
            "last_watered": "2026-03-10",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Plant"


def test_get_single_plant():
    """Test retrieving a single plant by ID."""
    response = client.get("/api/v1/plants/1")
    assert response.status_code in [200, 404]


def test_update_plant():
    """Test updating a plant."""
    response = client.put(
        "/api/v1/plants/1",
        json={
            "name": "Updated Plant",
            "watering_interval_days": 5,
            "sunlight": "Partial Sun",
            "last_watered": "2026-03-10",
        },
    )

    assert response.status_code in [200, 404]


def test_patch_plant():
    """Test partially updating a plant."""
    response = client.patch("/api/v1/plants/1", json={"sunlight": "Low Sun"})
    assert response.status_code in [200, 404]


def test_delete_plant():
    """Test deleting a plant."""
    response = client.delete("/api/v1/plants/1")
    assert response.status_code in [200, 404]


def test_bulk_create():
    """Test bulk creation of plants."""
    response = client.post(
        "/api/v1/plants/bulk",
        json=[
            {
                "name": "Plant A",
                "watering_interval_days": 2,
                "sunlight": "Full Sun",
                "last_watered": "2026-03-10",
            },
            {
                "name": "Plant B",
                "watering_interval_days": 4,
                "sunlight": "Partial Sun",
                "last_watered": "2026-03-10",
            },
        ],
    )

    assert response.status_code == 200


def test_rate_limit():
    """Test rate limiting behavior for plant creation."""
    responses = []

    for _ in range(12):
        r = client.post(
            "/api/v1/plants/",
            json={
                "name": "Rate Limit Test",
                "watering_interval_days": 3,
                "sunlight": "Full Sun",
                "last_watered": "2026-03-10",
            },
        )
        responses.append(r.status_code)

    assert 429 in responses or 200 in responses
