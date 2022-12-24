import pytest
from fastapi.encoders import jsonable_encoder
from sql_app.tests.utils.utils import random_string, random_email
from sql_app.crud.user_crud import *


def equal_seq(seq_1: list, seq_2: list):
    return all(
        a == b for a, b
        in zip(seq_1, seq_2, strict=True)
    )


def test_create_user(db: Session):
    email = random_email()
    password = random_string()
    tested_user = UserCreate(email=email, password=password)
    db_user = create_user(db=db, user=tested_user)
    assert db_user.email == email
    assert hasattr(db_user, 'hashed_pswd')


def test_get_user(db, get_and_create_user):
    # Create user at first
    db_user_2 = get_user(db, get_and_create_user.id)

    assert db_user_2
    assert db_user_2.email == get_and_create_user.email
    assert jsonable_encoder(db_user_2) == jsonable_encoder(get_and_create_user)


def test_get_user_by_email(db: Session, get_and_create_user):
    # Create user at first
    db_user_2 = get_user_by_email(db, get_and_create_user.email)

    assert db_user_2
    assert db_user_2.email == get_and_create_user.email
    assert jsonable_encoder(db_user_2) == jsonable_encoder(get_and_create_user)


def test_get_users(db: Session):
    number = 5
    email_list = (random_email() for _ in range(number))
    password_list = (random_string() for _ in range(number))
    users = [
        UserCreate(email=email, password=password)
        for email, password
        in zip(email_list, password_list)
    ]
    db_users = [
        create_user(db=db, user=user)
        for user in users
    ]
    tested_users = get_users(db=db)
    assert len(tested_users) == number
    assert equal_seq(db_users, tested_users)
