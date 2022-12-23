from starlette import status
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sql_app.schemas.user import User
from sql_app.schemas.token import TokenData
from sql_app.models import user
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sql_app.api.deps import get_db

SECRET_KEY = '2f2db14e6f82b71f39879d2f7e1d753b76d8c7a376aa6b057e6eb3215c03c19b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(email: str, db: Session):
    return db.query(user.User).filter(user.User.email == email).first()


def authenticate_user(email: str, password: str, db: Session) -> bool | User:
    user_dict = get_user(email=email, db=db)
    if not user_dict:
        return False
    if not verify_password(password, user_dict.hashed_pswd):
        return False
    return user_dict


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = expires_delta + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        print(e.args)
        raise credential_exception
    db_user = get_user(email=token_data.username, db=db)
    return db_user
