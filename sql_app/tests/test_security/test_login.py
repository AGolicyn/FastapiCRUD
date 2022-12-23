from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sql_app.crud.user_crud import create_user
from sql_app.schemas.user import UserCreate
import pytest


@pytest.fixture
def get_and_create_user(db: Session):
    test_user = {"email": "test@email", "password": "test_pass"}
    create_user(db=db, user=UserCreate(**test_user))
    return test_user


def test_login_with_correct_credentials(client: TestClient, get_and_create_user):
    # Create user at first
    test_user = get_and_create_user

    response = client.post("/token/", data={"username": "test@email", "password": "test_pass"})

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_login_with_invalid_username(client: TestClient, get_and_create_user):
    # Create user at first

    response = client.post("/token/", data={"username": "invalid_name", "password": "test_pass"})

    assert response.status_code == 401
    assert response.json()["detail"] == 'Incorrect username or password'


def test_login_with_invalid_password(client: TestClient, get_and_create_user):
    # Create user at first

    response = client.post("/token/", data={"username": "test@email", "password": "invalid_pass"})

    assert response.status_code == 401
    assert response.json()["detail"] == 'Incorrect username or password'
