from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sql_app.crud import item_crud
from sql_app.schemas import item


def test_delete_item(client: TestClient, db: Session, get_and_create_user):
    # Add item to current user
    created_item = item_crud.create_item(db=db,
                                         item=item.ItemCreate(**{"title": "some_title",
                                                                 "description": "some_description"}),
                                         user_id=get_and_create_user.id,
                                         current_user=get_and_create_user)
    assert len(get_and_create_user.items) == 1

    # Get access token
    token_response = client.post('/token', data={
        "username": get_and_create_user.email,
        "password": "test_pass"
    })
    token_response = token_response.json()

    # Delete item
    response = client.delete(f'/items/{get_and_create_user.items[0].id}', headers={
        'Authorization': f'Bearer {token_response["access_token"]}'
    })

    assert response.status_code == 200
    deleted_item = response.json()
    assert deleted_item["message"] == f'Deleted user {created_item.id}'

    response = client.get('/items')
    response = response.json()
    assert len(response) == 0


def test_update_item(client: TestClient, db: Session, get_and_create_user):
    # Add item to current user
    created_item = item_crud.create_item(db=db,
                                         item=item.ItemCreate(**{"title": "some_title",
                                                                 "description": "some_description"}),
                                         user_id=get_and_create_user.id,
                                         current_user=get_and_create_user)

    assert len(get_and_create_user.items) == 1

    # Get access token
    token_response = client.post('/token', data={
        "username": get_and_create_user.email,
        "password": "test_pass"
    })
    token_response = token_response.json()

    # Update item
    response = client.patch('/items/',
                            json={
                                "id": created_item.id,
                                "title": "New title",
                                "description": "New description"
                            },
                            headers={
                                'Authorization': f'Bearer {token_response["access_token"]}'
                            })
    assert response.status_code == 200
    new_data = response.json()
    assert new_data['title'] == "New title"
    assert new_data['description'] == "New description"
