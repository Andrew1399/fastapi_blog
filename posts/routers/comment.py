from fastapi import HTTPException, Depends, APIRouter, status, Response
from sqlalchemy.orm import Session
from database import get_db
from posts.schemas import CommentSchema, CommentCreateUpdate
from posts.models import Post, Comment
from users.models import User
from users.utils import get_current_user

router = APIRouter(prefix='/comments', tags=['Comments'])


@router.post('/{post_id}/create_comment')
def create_comment(request: CommentCreateUpdate, post_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id==post_id).first()
    new_comment = Comment(content=request.content, post_id=post_id, post=post, user_id=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get('/{post_id}')
def get_all_my_comments(post_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'Message': 'No such user'})
    comments = db.query(Comment).filter(Post.id==post_id, user_id=user.id).all()
    if comments is None:
        return {'Message': 'No comments added yet to this post'}
    return {'Details': f'{user.username}: comments: {comments}'}

@router.put('/{post_id}')
def update_comment(post_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id==post_id).first()
    comment = db.query(Comment).filter(post=post, user_id=user.id)
    comment.update(comment.dict(), synchronize_session=False)
    db.commit()
    return post

@router.delete('/{post_id}')
def delete_comment(post_id: int, db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    comment = db.query(Comment).filter(post=post, user_id=user.id)
    comment.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

