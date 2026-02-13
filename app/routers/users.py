from http import HTTPStatus
from pyexpat import model
from tarfile import NUL
from typing import List
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import EmailStr
from sqlalchemy import delete, select
from middlewares.auth import auth_middleware
from services.auth import create_access_token
from entities import models
from entities.models import User
from entities.schemas import AuthToken, UpdatePassword, UserCreate, UserGet
from services.database import get_db
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
user_router=APIRouter(prefix="/user")
user_router_protected = APIRouter(
    prefix="/user",
    tags=["protected"],dependencies=[Depends(auth_middleware)],
)


@user_router.get("/all", response_model=List[UserGet])
async def get_user(db: Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@user_router.post("/", status_code=HTTPStatus.CREATED)
async def create_user(new_user: UserCreate,db: Session=Depends(get_db)):
    user=models.User(**new_user.hash_pwd().dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return None

@user_router_protected.get("/{id}", response_model= UserGet)
async def get_user(id:int, request:Request,db: Session=Depends(get_db)):
    auth_user_id=request.state.auth_data["userID"]
    if(id!=auth_user_id):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="user unauthorized")
    stmt = select(models.User).filter(models.User.id == id) 
    user = db.scalar(stmt)

    return user

@user_router.post("/login", response_model=AuthToken)
async def login(login_info:UserCreate,db: Session=Depends(get_db)):
    stmt = select(models.User).filter(models.User.email == login_info.email)
    user = db.scalar(stmt)
    if(not(bcrypt.verify(login_info.password,user.password))):
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="pswed net metching")
    return {"token":create_access_token({"userID":user.id,"email":user.email})}

@user_router_protected.delete("/{id}" ,status_code=HTTPStatus.NO_CONTENT)
async def delete_user(id:int,request:Request,db:Session=Depends(get_db)):
    auth_user_id=request.state.auth_data["userID"]
    if(id!=auth_user_id):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="enetherezed eser")
    stmt=delete(models.User).where(models.User.id==id)
    db.execute(stmt)
    db.commit()
    return None

@user_router_protected.patch("/" ,status_code=HTTPStatus.NO_CONTENT)
async def update_password(user_info:UpdatePassword,request:Request,db:Session=Depends(get_db)):
    auth_email=request.state.auth_data["email"]
    user_email=user_info.email
    if user_email!=auth_email:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="emel net metching")
    
    stmt=select(models.User).filter(models.User.email==user_email)
    user=db.scalar(stmt)
    if (not(bcrypt.verify(user_info.old_pass,user.password))):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="old password is incorrect")
    db.query(models.User).filter(models.User.id==user.id).update({'password':bcrypt.hash(user_info.new_pass)})
    db.commit()
    return None



    
    
        

