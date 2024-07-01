import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from users.models import User


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    read_time = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User')
    comment = relationship('Comment')

    class Config:
        from_attributes = True


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post = relationship('Post')
    create_date = Column(DateTime, default=datetime.datetime.now)
