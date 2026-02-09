from http import HTTPStatus
from pyexpat import model
from tarfile import NUL
from typing import List
import bcrypt
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from services.auth import create_access_token
from entities import models
from entities.models import User
from entities.schemas import AuthToken, UserCreate, UserGet
from services.database import get_db
from passlib.hash import bcrypt

user_router=APIRouter()

@user_router.get("/users", response_model=List[UserGet])
async def get_user():
    db=get_db()
    users=db.query(models.User).all()
    return users

@user_router.post("/user", status_code=HTTPStatus.CREATED)
async def create_user(new_user: UserCreate):
    user=models.User(**new_user.hash_pwd().dict())
    db=get_db()
    db.add(user)
    db.commit()
    db.refresh(user)
    return None

@user_router.get("/user/{id}", response_model= UserGet)
async def get_user(id:int):
    db=get_db()
    stmt = select(models.User).filter(models.User.id == id)
    user = db.scalar(stmt)
    return user

@user_router.post("/user/login", response_model=AuthToken)
async def login(login_info:UserCreate):
    db=get_db()
    stmt = select(models.User).filter(models.User.email == login_info.email)
    user = db.scalar(stmt)
    if(not(bcrypt.verify(login_info.password,user.password))):
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="pswed net metching")
    return {"token":create_access_token({"userID":user.id,"email":user.email})}

    
        

