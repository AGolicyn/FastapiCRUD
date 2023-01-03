from fastapi import HTTPException
from sqlalchemy.orm import Session
from sql_app.models import models
from sql_app.schemas.item import ItemCreate, UpdateItem
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError

from sql_app.schemas.token import Status


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(models.Item).offset(skip).limit(limit)).scalars().all()


def create_item(db: Session, item: ItemCreate, user_id: int, current_user: models.User):
    if user_id == current_user.id:
        db_item = db.execute(insert(models.Item)
                             .values(title=item.title,
                                     description=item.description,
                                     owner_id=user_id)
                             .returning(models.Item)).scalar_one_or_none()
        db.commit()
        return db_item
    raise HTTPException(status_code=403, detail=f"Not authorized to delete")

def delete_item(db: Session, item_id: int, current_user: models.User):
    db_item: models.Item = db.execute(
        select(models.Item).where(models.Item.id == item_id)
    ).scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail=f'Item {item_id} does not exists')
    if db_item.owner_id == current_user.id:
        deleted_item_id = db.execute(delete(models.Item)
                                     .where(models.Item.id == item_id)
                                     .returning(models.Item.id)
                                     ).scalar_one_or_none()
        db.commit()
        if deleted_item_id:
            return Status(message=f'Deleted user {deleted_item_id}')
        raise HTTPException(status_code=404, detail=f'Item {item_id} does not exists')
    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


def update_item(db: Session, item: UpdateItem, current_user: models.User):
    db_item: models.Item = db.execute(
        select(models.Item).where(models.Item.id == item.id)
    ).scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail=f'Item {item.id} does not exists')
    if db_item.owner_id == current_user.id:
        updated_item = db.execute(update(models.Item)
                                  .where(models.Item.id == item.id)
                                  .values(title=item.title if item.title else db_item.title,
                                          description=item.description if item.description else db_item.description)
                                  .returning(models.Item)).scalar_one_or_none()
        db.commit()
        return updated_item
    raise HTTPException(status_code=403, detail=f"Not authorized to update")
