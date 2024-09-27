import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def new_user():
    return {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "testpassword",
        "role": "USER"
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


def test_register_user(test_client: TestClient, new_user: dict):
    response = test_client.post("/users/register", json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert data["username"], new_user["username"]


def test_register_existing_user(test_client: TestClient, new_user: dict):
    response = test_client.post("/users/register", json=new_user)
    assert response.status_code, 400


def test_login_user(test_client: TestClient, new_user: dict):
    login_data = {
        "username": new_user["username"],
        "password": new_user["password"]
    }
    response = test_client.post("/users/login", data=login_data)
    assert response.status_code, 200
    data = response.json()
    assert "access_token" in data


def test_invalid_user_login(test_client: TestClient, new_user: dict):
    login_data = {
        "username": "invalid",
        "password": "invalid"
    }
    response = test_client.post("/users/login", data=login_data)
    assert response.status_code, 401


def test_delete_non_existent_user_as_admin(test_client: TestClient, admin_token: str):
    response = test_client.delete("/users/99999", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code, 404


def test_delete_existent_user_as_admin(test_client: TestClient, admin_token: str, normal_user: dict):
    response = test_client.post("/users/register", json=normal_user)
    user_id = response.json()["id"]
    response = test_client.delete(f"/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code, 200
    response = test_client.delete(f"/users/{user_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code, 404


def test_delete_existent_user_as_normal_user(test_client: TestClient, normal_user_token: str):
    dummy_user = {
        "username": "dummy",
        "password": "dummy",
        "email": "dummy@test.com",
        "role": "USER"
    }
    response = test_client.post("/users/register", json=dummy_user)
    user_id = response.json()["id"]
    response = test_client.delete(f"/users/{user_id}", headers={"Authorization": f"Bearer {normal_user_token}"})
    assert response.status_code, 403
