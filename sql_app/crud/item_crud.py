from sqlalchemy.orm import Session
from sql_app.models.models import Item
from sql_app.schemas.item import ItemCreate
from sqlalchemy import select


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(Item).offset(skip).limit(limit)).scalars().all()


def create_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
