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
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)

    # Relationships
    categories = relationship('Category', back_populates='post')
    owner = relationship('User')
    comment = relationship('Comment')

    class Config:
        from_attributes = True

    def __str__(self):
        return self.title


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    post = relationship('Post')
    create_date = Column(DateTime, default=datetime.datetime.now)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    created = Column(DateTime, default=datetime.datetime.now)
    post = relationship('Post', back_populates='categories')
    def __str__(self):
        return self.slug
