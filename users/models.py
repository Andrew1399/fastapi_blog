from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class Token(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(500), primary_key=True)
    refresh_token = Column(String(500), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)
