from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sql_app.api.deps import get_db
from sql_app.schemas import item
from sql_app.crud import item_crud
router = APIRouter(
    tags=['item']
)

@router.post('/users/{user_id}/items', response_model=item.Item)
def create_item_for_user(item: item.ItemCreate, user_id: int, db: Session = Depends(get_db)):
    # todo Check if user exists and is authorized
    return item_crud.create_item(item=item, user_id=user_id, db=db)


@router.get('/items/', response_model=list[item.Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_items = item_crud.get_items(db=db, skip=skip, limit=limit)
    return db_items
