from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
import sql_app.core.security as security
from sql_app.core.security import authenticate_user
from sql_app.api.ap1_v1.api import api_router
from sql_app.api.deps import get_db
from sqlalchemy.orm import Session
from sql_app.schemas.token import Token
from sql_app.schemas.user import User
from sql_app.core.security import get_current_user
import sys

print(sys.path)
app = FastAPI()
app.include_router(api_router)


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     print('Вызван current active')
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail='Inactive user')
#     return current_user


@app.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "token_type": "bearer"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/')
def read_home(current_user: User = Depends(get_current_user)):
    return current_user
