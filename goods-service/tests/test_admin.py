def test_create_good_defaults(client):
    r = client.post("/admin/goods", json={"title": "Test Lamp", "price": 100.0})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test Lamp"
    assert data["is_visible"] == False
    assert data["quantity"] == 0


def test_admin_list_includes_invisible(client):
    client.post("/admin/goods", json={"title": "Visible", "price": 10.0, "is_visible": True})
    client.post("/admin/goods", json={"title": "Hidden", "price": 20.0})

    assert client.get("/admin/goods").json()["total"] == 2


def test_update_good(client):
    r = client.post("/admin/goods", json={"title": "Old", "price": 50.0})
    good_id = r.json()["good_id"]

    r = client.put(f"/admin/goods/{good_id}", json={"title": "New", "price": 75.0})
    assert r.status_code == 200
    assert r.json()["title"] == "New"
    assert r.json()["price"] == 75.0


def test_update_good_not_found(client):
    assert client.put("/admin/goods/999", json={"title": "X", "price": 10.0}).status_code == 404


def test_toggle_visibility(client):
    r = client.post("/admin/goods", json={"title": "Lamp", "price": 50.0})
    good_id = r.json()["good_id"]

    r = client.patch(f"/admin/goods/{good_id}/visibility", json={"is_visible": True})
    assert r.status_code == 200
    assert r.json()["is_visible"] == True


def test_delete_good(client):
    r = client.post("/admin/goods", json={"title": "To Delete", "price": 50.0})
    good_id = r.json()["good_id"]

    assert client.delete(f"/admin/goods/{good_id}").status_code == 204
    assert client.get("/admin/goods").json()["total"] == 0


def test_socle_crud(client):
    r = client.post("/admin/socles", json={"title": "E27"})
    assert r.status_code == 201
    socle_id = r.json()["socle_id"]

    assert client.put(f"/admin/socles/{socle_id}", json={"title": "E14"}).json()["title"] == "E14"
    assert client.delete(f"/admin/socles/{socle_id}").status_code == 204
    assert client.get("/admin/socles").json() == []


def test_shape_crud(client):
    r = client.post("/admin/shapes", json={"title": "Груша"})
    assert r.status_code == 201
    shape_id = r.json()["shape_id"]

    assert client.put(f"/admin/shapes/{shape_id}", json={"title": "Свеча"}).json()["title"] == "Свеча"
    assert client.delete(f"/admin/shapes/{shape_id}").status_code == 204


def test_type_crud(client):
    r = client.post("/admin/types", json={"title": "LED"})
    assert r.status_code == 201
    type_id = r.json()["type_id"]

    assert client.put(f"/admin/types/{type_id}", json={"title": "Галоген"}).json()["title"] == "Галоген"
    assert client.delete(f"/admin/types/{type_id}").status_code == 204


def test_supplier_link_and_unlink_good(client):
    supplier = client.post("/admin/suppliers", json={"name": "Philips"}).json()
    good = client.post("/admin/goods", json={"title": "Bulb", "price": 50.0}).json()
    sid, gid = supplier["supplier_id"], good["good_id"]

    r = client.post(f"/admin/suppliers/{sid}/goods", json={"good_id": gid})
    assert r.status_code == 201
    assert r.json()["message"] == "Связь создана"

    assert client.delete(f"/admin/suppliers/{sid}/goods/{gid}").status_code == 204


def test_supplier_link_duplicate_is_idempotent(client):
    supplier = client.post("/admin/suppliers", json={"name": "Osram"}).json()
    good = client.post("/admin/goods", json={"title": "Bulb", "price": 50.0}).json()
    sid, gid = supplier["supplier_id"], good["good_id"]

    client.post(f"/admin/suppliers/{sid}/goods", json={"good_id": gid})
    r = client.post(f"/admin/suppliers/{sid}/goods", json={"good_id": gid})
    assert r.status_code == 201