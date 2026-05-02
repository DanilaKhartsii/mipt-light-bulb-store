import pytest

ORDER_PAYLOAD = {
    "customer_name": "Иван Иванов",
    "customer_phone": "+79001234567",
    "customer_email": "ivan@example.com",
    "items": [{"good_id": 1, "quantity": 2}],
}


def test_create_order(client, mock_good):
    r = client.post("/orders", json=ORDER_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert data["customer_name"] == "Иван Иванов"
    assert data["status"] == "new"
    assert data["total_amount"] == pytest.approx(399.98)
    assert len(data["items"]) == 1
    assert data["items"][0]["good_sku"] == "GOOD-1"
    assert data["items"][0]["quantity"] == 2
    assert len(data["status_history"]) == 1
    assert data["status_history"][0]["new_status"] == "new"
    assert data["status_history"][0]["changed_by"] == "system"


def test_create_order_empty_items(client, mock_good):
    payload = {**ORDER_PAYLOAD, "items": []}
    assert client.post("/orders", json=payload).status_code == 422


def test_create_order_good_not_found(client, mock_good_not_found):
    r = client.post("/orders", json=ORDER_PAYLOAD)
    assert r.status_code == 422
    assert "не найден" in r.json()["detail"]


def test_create_order_goods_service_unavailable(client, mock_goods_unavailable):
    assert client.post("/orders", json=ORDER_PAYLOAD).status_code == 503


def test_get_order(client, mock_good):
    r = client.post("/orders", json=ORDER_PAYLOAD)
    order_id = r.json()["order_id"]

    r = client.get(f"/orders/{order_id}")
    assert r.status_code == 200
    assert r.json()["order_id"] == order_id


def test_get_order_not_found(client):
    assert client.get("/orders/999").status_code == 404


def test_order_multiple_items(client):
    good_stub_2 = {"good_id": 2, "title": "Лампа E14", "price": 99.50, "is_visible": True}
    from unittest.mock import patch

    def side_effect(good_id):
        return {"good_id": good_id, "title": f"Lamp {good_id}", "price": 100.0, "is_visible": True}

    with patch("app.services.order_service.fetch_good", side_effect=side_effect):
        payload = {
            **ORDER_PAYLOAD,
            "items": [{"good_id": 1, "quantity": 1}, {"good_id": 2, "quantity": 3}],
        }
        r = client.post("/orders", json=payload)

    assert r.status_code == 201
    data = r.json()
    assert len(data["items"]) == 2
    assert data["total_amount"] == pytest.approx(400.0)