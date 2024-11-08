from .database import Base
from sqlalchemy import Column, String, Integer

class BlogsTable(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String)
    body = Column(String)

class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index = True)
    name=Column(String)
    email=Column(String)
    password=Column(String)