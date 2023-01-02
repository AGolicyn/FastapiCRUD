from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sql_app.api.deps import get_db
from sql_app.schemas import item
from sql_app.crud import item_crud
from sql_app.schemas.token import Status
from sql_app.schemas import user
from sql_app.core.security import get_current_user

router = APIRouter(
    tags=['item']
)


@router.post('/users/{user_id}/items', response_model=item.Item)
def create_item_for_user(item: item.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    return item_crud.create_item(item=item, user_id=user_id, db=db)


@router.get('/items/', response_model=list[item.Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_items = item_crud.get_items(db=db, skip=skip, limit=limit)
    return db_items


@router.delete('/items/{item_id}', response_model=Status)
def delete_users_item(item_id: int, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    return item_crud.delete_item(db=db, item_id=item_id, current_user=current_user)


@router.patch('/items/', response_model=item.Item)
def update_item(item: item.UpdateItem,
                db: Session = Depends(get_db),
                current_user: user.User = Depends(get_current_user)):
    return item_crud.update_item(db=db, item=item, current_user=current_user)