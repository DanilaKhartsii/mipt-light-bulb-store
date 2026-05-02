def test_list_goods_empty(client):
    r = client.get("/goods")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_list_goods_only_visible(client):
    client.post("/admin/goods", json={"title": "Visible", "price": 100.0, "is_visible": True})
    client.post("/admin/goods", json={"title": "Hidden", "price": 50.0, "is_visible": False})

    data = client.get("/goods").json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Visible"


def test_get_visible_good(client):
    r = client.post("/admin/goods", json={"title": "LED E27", "price": 199.99, "is_visible": True})
    good_id = r.json()["good_id"]

    r = client.get(f"/goods/{good_id}")
    assert r.status_code == 200
    assert r.json()["price"] == 199.99


def test_get_invisible_good_returns_404(client):
    r = client.post("/admin/goods", json={"title": "Hidden", "price": 50.0, "is_visible": False})
    good_id = r.json()["good_id"]

    assert client.get(f"/goods/{good_id}").status_code == 404


def test_get_good_not_found(client):
    assert client.get("/goods/999").status_code == 404


def test_filter_by_min_price(client):
    client.post("/admin/goods", json={"title": "Cheap", "price": 10.0, "is_visible": True})
    client.post("/admin/goods", json={"title": "Expensive", "price": 500.0, "is_visible": True})

    data = client.get("/goods?min_price=100").json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Expensive"


def test_filter_by_max_price(client):
    client.post("/admin/goods", json={"title": "Cheap", "price": 10.0, "is_visible": True})
    client.post("/admin/goods", json={"title": "Expensive", "price": 500.0, "is_visible": True})

    data = client.get("/goods?max_price=50").json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Cheap"


def test_pagination(client):
    for i in range(5):
        client.post("/admin/goods", json={"title": f"Lamp {i}", "price": 10.0, "is_visible": True})

    page1 = client.get("/goods?page=1&limit=3").json()
    assert page1["total"] == 5
    assert len(page1["items"]) == 3

    page2 = client.get("/goods?page=2&limit=3").json()
    assert len(page2["items"]) == 2