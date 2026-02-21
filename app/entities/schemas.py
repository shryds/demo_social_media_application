import datetime
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt

class UserGet(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime.datetime

    class Config:
        orm_mode = True

class UserGetEmail(BaseModel):
    email:EmailStr

    class Config:
        orm_mode = True


class PostGet(BaseModel):
    id: int
    title:str
    content:str  
    published:bool 
    created_at: datetime.datetime
    user: UserGetEmail
    
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title:str
    content:str 

class UserCreate(BaseModel):
    email: EmailStr
    password:str
    def hash_pwd(self):
        self.password=bcrypt.hash(self.password)
        return self


class AuthToken(BaseModel):
    token:str

    
class UpdatePassword(BaseModel):
    email:EmailStr
    old_pass:str
    new_pass:str

class CommentCreate(BaseModel):
    comment:str
    
class GetComments(BaseModel):
    id:int
    commenter_id:int
    comment:str
    post_id:int
    created_at:datetime.datetime
    user: UserGetEmail
    
    class Config:
        orm_mode = True