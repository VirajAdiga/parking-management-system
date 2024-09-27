import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def new_parking_slot():
    return {
        "label": "SLOT1"
    }


@pytest.fixture(scope="module")
def admin_user():
    return {
        "username": "admin",
        "email": "admin@test.com",
        "password": "password",
        "role": "ADMIN"
    }


@pytest.fixture(scope="module")
def normal_user():
    return {
        "username": "user",
        "email": "user@test.com",
        "password": "user",
        "role": "USER"
    }


@pytest.fixture(scope="module")
def admin_token(test_client: TestClient, admin_user: dict):
    test_client.post("/users/register", json=admin_user)
    response = test_client.post("/users/login", data={"username": admin_user["username"], "password": admin_user["password"]})
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def normal_user_token(test_client: TestClient, normal_user: dict):
    test_client.post("/users/register", json=normal_user)
    response = test_client.post("/users/login", data={"username": normal_user["username"], "password": normal_user["password"]})
    return response.json()["access_token"]


def test_create_parking_slot_as_normal_user(test_client: TestClient, normal_user_token: str, new_parking_slot: dict):
    response = test_client.post("/parking-slots/", json=new_parking_slot, headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 403


def test_create_parking_slot_as_admin(test_client: TestClient, admin_token: str, new_parking_slot: dict):
    response = test_client.post("/parking-slots/", json=new_parking_slot, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == new_parking_slot["label"]


def test_get_all_available_slots_as_normal_user(test_client: TestClient, admin_token: str, normal_user_token: str, new_parking_slot: dict):
    parking_slot = {
        "label": "SLOT2"
    }
    test_client.post("/parking-slots/", json=parking_slot, headers={"Authorization": f"Bearer {admin_token}"})
    response = test_client.get("/parking-slots/", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_move_parking_slot_to_maintenance(test_client: TestClient, admin_token: str, normal_user_token: str):
    response = test_client.put("/parking-slots/2", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UNDER_MAINTENANCE"
    response = test_client.get("/parking-slots/", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_delete_parking_slot_as_admin(test_client: TestClient, admin_token: str, normal_user_token: str):
    response = test_client.delete("/parking-slots/2", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    response = test_client.get("/parking-slots/", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
