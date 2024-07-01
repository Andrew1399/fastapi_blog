import datetime
from pydantic import BaseModel
from users.schemas import UserSchema

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    read_time: int
    owner_id: int
    owner: UserSchema


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool
    read_time: int


class PostUpdate(BaseModel):
    title: str
    content: str
    read_time: int

class CommentSchema(BaseModel):
    id: int
    content: str
    user_id: int
    user: UserSchema
    post_id: int
    post: PostSchema
    created_at: datetime.datetime

class CommentCreateUpdate(BaseModel):
    user_id: int
    post_id: int
    content: str

