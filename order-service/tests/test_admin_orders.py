ORDER_PAYLOAD = {
    "customer_name": "Тест Тестов",
    "customer_phone": "+79009998877",
    "customer_email": "test@example.com",
    "items": [{"good_id": 1, "quantity": 1}],
}


def _create_order(client):
    return client.post("/orders", json=ORDER_PAYLOAD).json()


def test_list_orders_empty(client):
    r = client.get("/admin/orders")
    assert r.status_code == 200
    assert r.json()["total"] == 0


def test_list_orders(client, mock_good):
    _create_order(client)
    assert client.get("/admin/orders").json()["total"] == 1


def test_list_orders_by_status(client, mock_good):
    _create_order(client)
    assert client.get("/admin/orders?status=new").json()["total"] == 1
    assert client.get("/admin/orders?status=processing").json()["total"] == 0


def test_list_orders_invalid_status(client):
    assert client.get("/admin/orders?status=invalid").status_code == 422


def test_change_order_status(client, mock_good):
    order_id = _create_order(client)["order_id"]

    r = client.patch(f"/admin/orders/{order_id}/status", json={"status": "processing"})
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "processing"
    assert len(data["status_history"]) == 2


def test_status_transition_new_to_completed_invalid(client, mock_good):
    order_id = _create_order(client)["order_id"]

    r = client.patch(f"/admin/orders/{order_id}/status", json={"status": "completed"})
    assert r.status_code == 422
    assert "недопустим" in r.json()["detail"]


def test_full_order_lifecycle(client, mock_good):
    order_id = _create_order(client)["order_id"]

    client.patch(f"/admin/orders/{order_id}/status", json={"status": "processing"})
    r = client.patch(
        f"/admin/orders/{order_id}/status",
        json={"status": "completed", "change_reason": "Доставлен"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
    assert len(r.json()["status_history"]) == 3


def test_cancel_from_new(client, mock_good):
    order_id = _create_order(client)["order_id"]

    r = client.patch(f"/admin/orders/{order_id}/status", json={"status": "cancelled"})
    assert r.status_code == 200
    assert r.json()["status"] == "cancelled"


def test_change_status_order_not_found(client):
    r = client.patch("/admin/orders/999/status", json={"status": "processing"})
    assert r.status_code == 404


def test_admin_get_order(client, mock_good):
    order_id = _create_order(client)["order_id"]

    r = client.get(f"/admin/orders/{order_id}")
    assert r.status_code == 200
    assert r.json()["order_id"] == order_id