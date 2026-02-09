import datetime
import email
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt


class PostGet(BaseModel):
    id: int
    title:str
    content:str  
    published:bool 
    created_at: datetime.datetime
    
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

class UserGet(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime.datetime

    class Config:
        orm_mode = True


class AuthToken(BaseModel):
    token:str

    

