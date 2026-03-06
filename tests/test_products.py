import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_product():

    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "Testing product",
            "price": 100,
            "quantity": 5
        }
    )

    assert response.status_code in [200, 201]


def test_get_products():

    response = client.get("/products/")

    assert response.status_code == 200

def test_get_product_not_found():

    response = client.get("/products/99999")

    assert response.status_code == 404