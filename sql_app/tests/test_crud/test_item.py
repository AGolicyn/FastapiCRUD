import pytest

from sql_app.tests.utils.utils import random_string
from sql_app.crud.item_crud import *
from sql_app.crud.user_crud import *
from sql_app.models.models import User


def test_create_item(db: Session, get_and_create_user):
    # Create user at first

    # Create item to add
    title = random_string()
    description = random_string()
    item = ItemCreate(title=title, description=description)

    item_db = create_item(db=db, item=item, user_id=get_and_create_user.id)

    assert item_db.title == title
    assert item_db.description == description
    assert item_db.owner_id == get_and_create_user.id


def test_get_items(db, get_and_create_user):
    # Create item to add
    title = random_string()
    description = random_string()
    item = ItemCreate(title=title, description=description)
    create_item(db=db, item=item, user_id=get_and_create_user.id)

    test_item = get_items(db=db)

    assert len(test_item) == 1
    test_item = test_item[0]
    assert test_item.title == title
    assert test_item.description == description
    assert test_item.owner_id == get_and_create_user.id


def test_delete_item(db, fill_db_with_data):
    data: User = fill_db_with_data[0]
    item_id_to_delete = data.items[0].id
    assert len(data.items) == 2

    deleted_id = delete_item(db=db, item_id=item_id_to_delete, current_user=data)

    assert len(data.items) == 1
    assert str(item_id_to_delete) in deleted_id.message


def test_delete_item_with_invalid_id(db, fill_db_with_data):
    data = fill_db_with_data

    with pytest.raises(HTTPException):
        delete_item(db=db, item_id=0, current_user=data[0])

    assert len(data[0].items) == 2
    assert len(data[1].items) == 2


def test_delete_item_by_unauthorized_user(db, fill_db_with_data):
    data = fill_db_with_data

    class fake_user:
        id: 0

    with pytest.raises(HTTPException):
        delete_item(db=db, item_id=data[0].id, current_user=fake_user)

    assert len(data[0].items) == 2
    assert len(data[1].items) == 2
