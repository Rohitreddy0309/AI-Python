import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)


def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "Testing product",
            "price": 100,
            "quantity": 5,
        },
    )

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["name"] == "Test Product"


def test_bulk_create_products():
    response = client.post(
        "/products/",
        json=[
            {
                "name": "Bulk Product 1",
                "description": "Bulk test",
                "price": 50,
                "quantity": 10,
            },
            {
                "name": "Bulk Product 2",
                "description": "Bulk test",
                "price": 60,
                "quantity": 20,
            },
        ],
    )

    assert response.status_code in [200, 201]


def test_get_all_products():
    response = client.get("/products/")
    assert response.status_code == 200


def test_get_product_not_found():
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_update_product():
    create = client.post(
        "/products/",
        json={
            "name": "Update Test",
            "description": "Before update",
            "price": 200,
            "quantity": 3,
        },
    )

    product_id = create.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Product",
            "description": "After update",
            "price": 300,
            "quantity": 4,
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"


def test_delete_product():
    create = client.post(
        "/products/",
        json={
            "name": "Delete Test",
            "description": "Delete me",
            "price": 10,
            "quantity": 1,
        },
    )

    product_id = create.json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200


def test_bulk_update():
    create = client.post(
        "/products/",
        json={"name": "Bulk Update", "description": "Test", "price": 10, "quantity": 1},
    )

    product_id = create.json()["id"]

    response = client.put(
        "/products/",
        json=[
            {
                "id": product_id,
                "name": "Bulk Updated",
                "description": "Updated",
                "price": 20,
                "quantity": 2,
            }
        ],
    )

    assert response.status_code == 200


def test_bulk_delete():
    create = client.post(
        "/products/",
        json={
            "name": "Bulk Delete",
            "description": "Delete",
            "price": 5,
            "quantity": 1,
        },
    )

    product_id = create.json()["id"]

    response = client.request("DELETE", "/products/", json=[product_id])

    assert response.status_code == 200
