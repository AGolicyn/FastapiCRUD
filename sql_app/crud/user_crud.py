from sqlalchemy.orm import Session
from sqlalchemy import select
from sql_app.models import models
from sql_app.schemas.user import UserCreate
from sql_app.core.security import get_password_hash


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
    db_user = models.User(email=user.email, hashed_pswd=hashed_pswd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
