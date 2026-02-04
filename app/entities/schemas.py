import datetime
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
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

class UserGet(UserCreate):
    id:int
    created_at:datetime.datetime

    class Config:
        orm_mode = True


    

