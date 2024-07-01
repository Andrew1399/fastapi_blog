import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
import jwt
from users.schemas import TokenData
from users.models import User
from database import get_db
from .env import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = 'HS256'
JWT_SECRET_KEY = JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = JWT_REFRESH_SECRET_KEY

password_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# Logic to create jwt token when user logins in

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: int=None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'exp': expires_delta, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            return credentials_exception
        username = payload.get('sub')
        return TokenData(id=user_id, username=username)
    except:
        raise credentials_exception

def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials')
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id==token.id).first()
    return user
