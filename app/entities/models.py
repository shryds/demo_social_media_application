import email
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Boolean,TIMESTAMP,text
from app.services.database import Base

class Posts(Base):
    __tablename__='posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default=text('now()'))
    user_id= Column(Integer,ForeignKey("users.id"), nullable=False )
    

class User(Base):
    __tablename__="users"

    email= Column(String, unique=True)
    password = Column(String, unique=True)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default=text('now()') )