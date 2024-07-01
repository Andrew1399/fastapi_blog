from fastapi import FastAPI, Depends
from posts.models import Post
from posts.schemas import PostSchema
from database import engine, SessionLocal, Base, get_db
from sqlalchemy.orm import Session
from posts.routers import post, comment
from users.routers import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)
