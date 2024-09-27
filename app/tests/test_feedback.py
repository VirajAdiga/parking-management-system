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


def test_create_feedback_as_normal_user(test_client: TestClient, normal_user_token: str, admin_token: str, new_parking_slot: dict):
    response = test_client.post("/parking-slots/", json=new_parking_slot, headers={"Authorization": f"Bearer {admin_token}"})
    data = response.json()
    assert response.status_code == 200

    booking_data = {
        "slot_id": data["id"],
        "start_date": "2023-01-01",
        "end_date": "2023-01-01"
    }
    response = test_client.get("/parking-slots/", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = test_client.post(
        "/bookings/",
        json=booking_data,
        headers={"Authorization": f"Bearer {normal_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["slot_id"] == booking_data["slot_id"]

    feedback_data = {
        "booking_id": data["id"],
        "rating": 4,
        "comment": "Good service"
    }

    response = test_client.post("/feedbacks/", json=feedback_data, headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["booking_id"] == feedback_data["booking_id"]


def test_get_all_feedbacks_of_user(test_client: TestClient, normal_user_token: str):
    response = test_client.get("/feedbacks/", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1