from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_delete_item(client: TestClient, db: Session, get_and_create_user):
    # Add item to current user
    created_item = client.post(f'/users/{get_and_create_user.id}/items', json={
        "title": "some_title",
        "description": "some_description"
    })
    created_item = created_item.json()
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
    assert deleted_item["message"] == f'Deleted user {created_item["id"]}'

    response = client.get('/items')
    response = response.json()
    assert len(response) == 0

