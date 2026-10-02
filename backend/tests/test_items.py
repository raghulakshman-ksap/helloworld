from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_get_item():
    created = client.post("/items", json={"name": "Widget", "price": 9.5})
    assert created.status_code == 201
    item = created.json()
    assert client.get(f"/items/{item['id']}").json() == item


def test_invalid_price_rejected():
    assert client.post("/items", json={"name": "Bad", "price": 0}).status_code == 422


def test_missing_item_404():
    assert client.get("/items/9999").status_code == 404
