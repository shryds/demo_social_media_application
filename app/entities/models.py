from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,Boolean,TIMESTAMP, null,text
from app.services.database import Base
from sqlalchemy.orm import relationship

class Posts(Base):
    __tablename__='posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default=text('now()'))
    user_id= Column(Integer,ForeignKey("users.id"), nullable=False )
    likes=Column(Integer,nullable=False,server_default="0")
    user = relationship("User")
    img_path=Column(String,unique=True)

class User(Base):
    __tablename__="users"

    email= Column(String, unique=True)
    password = Column(String, unique=True)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default=text('now()') )

class Like(Base):
    __tablename__="likes"

    post_id=Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),nullable=False,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"), nullable=False,primary_key=True)

class Comment(Base):
    __tablename__="comments"

    id=Column(Integer, primary_key=True, nullable=False)
    post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    commenter_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    comment=Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable =False, server_default=text('now()') )
    user = relationship("User")

