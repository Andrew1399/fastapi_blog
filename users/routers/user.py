from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from functools import wraps
from sqlalchemy.orm import Session
from datetime import datetime
from users import schemas
from sqlalchemy.orm import Session
from users.schemas import UserSchema, TokenSchema, RequestDetails
from users.models import User, Token
from database import get_db
from users.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password
from database import Base
from users.auth_bearer import JWTBearer
from users.utils import JWT_SECRET_KEY, ALGORITHM

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register')
def register(user: UserSchema, db: Session=Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = User(username=user.username, email=user.email, password=encrypted_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"user {user.username} created successfully"}


@router.post('/login', response_model=schemas.TokenSchema)
def login(request: schemas.RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = Token(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@router.get('/getusers')
def get_users(dependencies=Depends(JWTBearer()), db: Session=Depends(get_db)):
    user = db.query(User).all()
    return user


@router.post('/change_password')
def change_password(request: schemas.ChangePassword, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.email==request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user not found')
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid old password')
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    return {'Message': 'Password changed successfully'}


@router.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(Token).all()
    info = []
    for record in token_record:
        print('record', token_record)
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(user_id)
    if info:
        existing_token = db.query(Token).where(Token.user_id.in_(info)).delete()
        db.commit()
    existing_token = db.query(Token).filter(Token.user_id==user_id, Token.access_token==token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {'Message': 'Logout successfully'}


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        data = kwargs['session'].query(Token).filter_by(user_id=user_id, access_toke=kwargs['dependencies'],
                                                                    status=True).first()
        if data:
            return func(kwargs['dependencies'], kwargs['session'])

        else:
            return {'msg': "Token blocked"}

    return wrapper

