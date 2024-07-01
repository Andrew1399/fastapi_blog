from pydantic import BaseModel
import datetime


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RequestDetails(BaseModel):
    email: str
    password: str


class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime.datetime


class TokenData(BaseModel):
    user_id: int
    username: str
