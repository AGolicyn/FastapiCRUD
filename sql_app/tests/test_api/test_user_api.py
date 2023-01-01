import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sql_app.tests.utils.utils import random_email
from sql_app.crud.user_crud import create_user
from sql_app.schemas.user import UserCreate

user_email = random_email()


def test_create_user(client: TestClient, db: Session):
    response = client.post(
        "/users/",
        json={"email": user_email, "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == user_email
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == user_email
    assert data["id"] == user_id


def test_create_user_with_duplicate_email(client: TestClient, db: Session, get_and_create_user):
    in_base_email = get_and_create_user.email
    response = client.post(
        "/users/",
        json={"email": in_base_email, "password": "chimichangas4life"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Sorry, this username already exists."


def test_get_one_user(client: TestClient, db: Session, fill_db_with_data):
    '''Check '''
    db_user = [*fill_db_with_data]
    response = client.get(f"/users/{db_user[0].id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == db_user[0].email
    assert data["id"] == db_user[0].id
    assert len(data["items"]) == 2

    # Проверяем каждое поле отдельно
    assert data["items"][0]["title"] == "test_title_1_user_1"
    assert data["items"][0]["description"] == "test_description_1_user_1"
    assert data["items"][0]["owner_id"] == db_user[0].id
    assert data["items"][1]["title"] == "test_title_2_user_1"
    assert data["items"][1]["description"] == "test_description_2_user_1"
    assert data["items"][1]["owner_id"] == db_user[0].id


def test_get_user_with_invalid_id(db: Session, client: TestClient):
    response = client.get(f"/users/{0}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User does not exists"


def test_delete_user_by_id(db: Session, client: TestClient, get_and_create_user):
    # Create user and authorize
    token_response = client.post(f"/token", data={
        "username": get_and_create_user.email,
        "password": "test_pass"
    })
    token_response = token_response.json()

    response = client.delete(f"/users/{get_and_create_user.id}", headers={
        'Authorization': f'Bearer {token_response["access_token"]}'
    })

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Deleted user {get_and_create_user.id}"
    # assert data["username"] == get_and_create_user.username

    response = client.get(f"/users/{get_and_create_user.id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == 'User does not exists'


def test_delete_user_by_unauthorized_user(db: Session, client: TestClient, get_and_create_user):
    response = client.delete(f'/users/{get_and_create_user.id}')
    assert response.status_code == 401
    data = response.json()
    assert data['detail'] == "Not authenticated"


def test_delete_user_with_incorrect_id(db: Session, client: TestClient, get_and_create_user):
    # Create user and authorize
    token_response = client.post(f"/token", data={
        "username": get_and_create_user.email,
        "password": "test_pass"
    })
    token_response = token_response.json()

    response = client.delete(f"/users/0", headers={
        'Authorization': f'Bearer {token_response["access_token"]}'
    })

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User 0 not found"


def test_delete_user_by_another_authenticated_user(db: Session, client: TestClient, get_and_create_user):
    # Create user and authorize
    token_response = client.post(f"/token", data={
        "username": get_and_create_user.email,
        "password": "test_pass"
    })
    token_response = token_response.json()

    # Create another user
    db_user = create_user(
        db=db, user=UserCreate(email='another-test@gmail.com', password='test_pass'))

    response = client.delete(f"/users/{db_user.id}", headers={
        'Authorization': f'Bearer {token_response["access_token"]}'
    })

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Not authorized to delete"
