def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_device_type(client):
    response = client.post("/device-types", json={"name": "Relay-A", "description": "Demo relay"})
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Relay-A"

    response = client.get(f"/device-types/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Relay-A"


def test_duplicate_device_type_returns_409(client):
    client.post("/device-types", json={"name": "Relay-A"})
    response = client.post("/device-types", json={"name": "Relay-A"})
    assert response.status_code == 409


def test_create_device(client):
    device_type = client.post("/device-types", json={"name": "Relay-A"}).json()
    response = client.post("/devices", json={"name": "relay-001", "device_type_id": device_type["id"]})
    assert response.status_code == 201
    assert response.json()["device_type_id"] == device_type["id"]
    assert len(client.get("/devices").json()) == 1


def test_device_with_unknown_type_returns_404(client):
    response = client.post("/devices", json={"name": "relay-001", "device_type_id": 999})
    assert response.status_code == 404


def test_missing_device_returns_404(client):
    assert client.get("/devices/12345").status_code == 404


def test_empty_name_is_rejected(client):
    response = client.post("/device-types", json={"name": ""})
    assert response.status_code == 422
