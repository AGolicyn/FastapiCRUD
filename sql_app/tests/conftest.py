import pytest
from fastapi.testclient import TestClient
from sqlalchemy.sql import text

from sql_app.db.session import *
from sql_app.main import *
from sql_app.models import models
from sql_app.tests.utils.utils import random_email

SQLALCHEMY_TESTBASE_URL = "postgresql://artem:123@localhost:5432/test"
engine = create_engine(SQLALCHEMY_TESTBASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
table_names = ', '.join(Base.metadata.tables.keys())


def override_get_db():
    """Временное соединение для одного endpoint'а"""
    db_temp = TestingSessionLocal()
    try:
        yield db_temp
    finally:
        db_temp.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    """Cоединение от начала и до конца теста, очищает базу по завершению"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.execute(text('TRUNCATE users, items CASCADE'))
        db.commit()
        db.close()


@pytest.fixture(scope='module')
def client():
    yield TestClient(app)


@pytest.fixture
def fill_db_with_data(db: Session):
    db_user_1 = models.User(email=random_email(), hashed_pswd='test_pass')
    db_user_2 = models.User(email=random_email(), hashed_pswd='test_pass_2')
    db.add(db_user_1)
    db.add(db_user_2)
    db.commit()
    db.refresh(db_user_1)
    db.refresh(db_user_2)

    db_item_1_1 = models.Item(title='test_title_1_user_1',
                              description='test_description_1_user_1',
                              owner_id=db_user_1.id)
    db_item_1_2 = models.Item(title='test_title_2_user_1',
                              description='test_description_2_user_1',
                              owner_id=db_user_1.id)
    db_item_2_1 = models.Item(title='test_title_1_user_2',
                              description='test_description_1_user_2',
                              owner_id=db_user_2.id)
    db_item_2_2 = models.Item(title='test_title_2_user_1',
                              description='test_description_2_user_2',
                              owner_id=db_user_2.id)

    for item in (db_item_1_1, db_item_1_2, db_item_2_1, db_item_2_2):
        db.add(item)
    db.commit()
    return db_user_1, db_user_2


@pytest.fixture
def get_and_create_user(db: Session):
    from sql_app.crud.user_crud import create_user
    from sql_app.schemas.user import UserCreate

    test_user = {"email": random_email(), "password": "test_pass"}
    db_user = create_user(db=db, user=UserCreate(**test_user))
    return db_user
