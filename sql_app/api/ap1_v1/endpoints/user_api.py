from fastapi import APIRouter, Depends, HTTPException
from sql_app.schemas import user, token
from sql_app.crud import user_crud
from sql_app.api.deps import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sql_app.core.security import get_current_user

router = APIRouter(
    prefix='/users',
    tags=["user"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/', response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db=db, user=user)
    return db_user


@router.get('/', response_model=list[user.User], dependencies=[Depends(get_current_user)])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = user_crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@router.get('/{user_id}', response_model=user.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User does not exists')
    return db_user


@router.delete('/{user_id}', response_model=token.Status)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    return user_crud.delete_user_by_id(db=db, current_user=current_user, user_id=user_id)
