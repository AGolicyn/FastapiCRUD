from fastapi.testclient import TestClient


def test_login_with_correct_credentials(client: TestClient, get_and_create_user):
    # Create user at first
    test_user = get_and_create_user

    response = client.post("/token/", data={"username": test_user.email, "password": "test_pass"})

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_login_with_invalid_username(client: TestClient, get_and_create_user):
    # Create user at first
    response = client.post("/token/", data={"username": "invalid_name", "password": 'test_pass'})

    assert response.status_code == 401
    assert response.json()["detail"] == 'Incorrect username or password'


def test_login_with_invalid_password(client: TestClient, get_and_create_user):
    # Create user at first

    response = client.post("/token/", data={"username": get_and_create_user.email, "password": "invalid_pass"})

    assert response.status_code == 401
    assert response.json()["detail"] == 'Incorrect username or password'
