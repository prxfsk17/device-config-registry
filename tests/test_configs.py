def post_config(client, device_id, parameters, comment=None):
    return client.post(
        f"/devices/{device_id}/configs",
        json={"parameters": parameters, "comment": comment},
    )


def test_versions_are_numbered_from_one(client, device):
    first = post_config(client, device["id"], {"threshold": 10})
    second = post_config(client, device["id"], {"threshold": 12}, "raised threshold")
    assert first.status_code == 201
    assert first.json()["version"] == 1
    assert second.json()["version"] == 2
    assert second.json()["comment"] == "raised threshold"


def test_versions_are_counted_per_device(client, device):
    other_type = client.post("/device-types", json={"name": "Relay-B"}).json()
    other = client.post(
        "/devices", json={"name": "relay-002", "device_type_id": other_type["id"]}
    ).json()
    post_config(client, device["id"], {"a": 1})
    post_config(client, device["id"], {"a": 2})
    assert post_config(client, other["id"], {"a": 1}).json()["version"] == 1


def test_list_get_and_latest(client, device):
    post_config(client, device["id"], {"a": 1})
    post_config(client, device["id"], {"a": 2})

    versions = client.get(f"/devices/{device['id']}/configs").json()
    assert [c["version"] for c in versions] == [1, 2]

    assert client.get(f"/devices/{device['id']}/configs/1").json()["parameters"] == {"a": 1}
    assert client.get(f"/devices/{device['id']}/configs/latest").json()["version"] == 2


def test_diff_between_versions(client, device):
    post_config(client, device["id"], {"threshold": 10, "mode": "auto", "legacy": True})
    post_config(client, device["id"], {"threshold": 12, "mode": "auto", "timeout": 30})

    response = client.get(
        f"/devices/{device['id']}/configs/diff", params={"from_version": 1, "to_version": 2}
    )
    assert response.status_code == 200
    assert response.json() == {
        "from_version": 1,
        "to_version": 2,
        "added": {"timeout": 30},
        "removed": {"legacy": True},
        "changed": {"threshold": {"old": 10, "new": 12}},
    }


def test_unknown_device_returns_404(client):
    assert post_config(client, 999, {"a": 1}).status_code == 404
    assert client.get("/devices/999/configs").status_code == 404


def test_unknown_version_returns_404(client, device):
    post_config(client, device["id"], {"a": 1})
    assert client.get(f"/devices/{device['id']}/configs/5").status_code == 404
    response = client.get(
        f"/devices/{device['id']}/configs/diff", params={"from_version": 1, "to_version": 5}
    )
    assert response.status_code == 404


def test_latest_without_configs_returns_404(client, device):
    assert client.get(f"/devices/{device['id']}/configs/latest").status_code == 404


def test_empty_parameters_are_rejected(client, device):
    assert post_config(client, device["id"], {}).status_code == 422
