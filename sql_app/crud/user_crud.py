from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, insert, update
from sql_app.models import models
from sql_app.schemas.user import UserCreate, UserBase
from sql_app.schemas.token import Status
from sql_app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError


def get_user(db: Session, user_id: int):
    return db.execute(select(models.User)
                      .filter(models.User.id == user_id)).scalar_one_or_none()


def get_user_by_email(db: Session, email: str):
    return db.execute(select(models.User)
                      .filter(models.User.email == email)).scalar_one_or_none()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.execute(select(models.User).offset(skip).limit(limit)).scalars().all()


def create_user(db: Session, user: UserCreate):
    hashed_pswd = get_password_hash(user.password)
    try:
        db_user = db.execute(insert(models.User)
                             .values(email=user.email, hashed_pswd=hashed_pswd)
                             .returning(models.User)).scalar_one_or_none()
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=401, detail=f"Sorry, this username already exists.")
    return db_user


def delete_user_by_id(db: Session, current_user, user_id: int):
    db_user = db.execute(select(models.User)
                         .filter(models.User.id == user_id)).scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    if db_user.id == current_user.id:
        deleted_user_id = db.execute(delete(models.User)
                                     .where(models.User.id == user_id)
                                     .returning(models.User.id)).scalar_one_or_none()
        db.commit()
        if deleted_user_id:
            return Status(message=f'Deleted user {deleted_user_id}')
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")

