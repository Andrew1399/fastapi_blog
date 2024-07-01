from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from posts.schemas import PostSchema, PostCreate, PostUpdate
from posts.models import Post
from users.models import User
from database import get_db
from users.utils import get_current_user

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/posts', status_code=status.HTTP_200_OK)
def get_posts(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    posts = db.query(Post).all()
    return posts


@router.get('/{post_id}', status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id==post_id).first()
    if post is None:
        return {'Message': f'There is no post with {post_id} id'}
    return post


@router.post('/add_post', status_code=status.HTTP_201_CREATED)
def add_post(request: PostSchema, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    new_post = Post(owner_id=user.id, title=request.title, content=request.content, published=request.published,
                    read_time=request.read_time)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put('/update_post/{post_id}', status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: PostUpdate, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    db_post.title = post.title
    db_post.content = post.content
    db_post.read_time = post.read_time
    db.commit()
    return db_post

@router.delete('/delete_post/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    db.delete(db_post)
    db.commit()
    db.close()
