from http import HTTPStatus
from pyexpat import model
from tarfile import NUL
from typing import List
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import EmailStr
from sqlalchemy import and_, delete, exists, select
from app.middlewares.auth import auth_middleware
from app.services.auth import create_access_token
from app.entities import models
from app.entities.models import User
from app.entities.schemas import AuthToken, GetComments, PostGet, PostGetUser, UpdatePassword, UserCreate, UserGet
from app.services.database import get_db
from passlib.hash import bcrypt
from sqlalchemy.orm import Session, joinedload
user_router=APIRouter(prefix="/user")
user_router_protected = APIRouter(
    prefix="/user",
    tags=["protected"],dependencies=[Depends(auth_middleware)],
)


@user_router.post("/login", response_model=AuthToken)
async def login(login_info:UserCreate,db: Session=Depends(get_db)):
    stmt = select(models.User).filter(models.User.email == login_info.email)
    user = db.scalar(stmt)
    
    if(user == None):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No account is registered with this email address")

    if(not(bcrypt.verify(login_info.password,user.password))):
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Incorrect password")

    return {"token":create_access_token({"userID":user.id,"email":user.email})}

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
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="You are not authorized to access this user")
    stmt = select(models.User).filter(models.User.id == id) 
    user = db.scalar(stmt)

    return user


@user_router_protected.delete("/{id}" ,status_code=HTTPStatus.NO_CONTENT)
async def delete_user(id:int,request:Request,db:Session=Depends(get_db)):
    auth_user_id=request.state.auth_data["userID"]
    if(id!=auth_user_id):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="You are not authorized to delete this user")
    stmt=delete(models.User).where(models.User.id==id)
    db.execute(stmt)
    db.commit()
    return None

@user_router_protected.patch("/" ,status_code=HTTPStatus.NO_CONTENT)
async def update_password(user_info:UpdatePassword,request:Request,db:Session=Depends(get_db)):
    auth_email=request.state.auth_data["email"]
    user_email=user_info.email
    if user_email!=auth_email:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email does not match the authenticated user")
    
    stmt=select(models.User).filter(models.User.email==user_email)
    user=db.scalar(stmt)
    if (not(bcrypt.verify(user_info.old_pass,user.password))):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Current password is incorrect")
    db.query(models.User).filter(models.User.id==user.id).update({'password':bcrypt.hash(user_info.new_pass)})
    db.commit()
    return None

@user_router_protected.get("/auth/me")
async def update_password(request:Request):
    auth_email=request.state.auth_data["email"]
    auth_id=request.state.auth_data["userID"]

    return {
        "email":auth_email,
        "user_id":auth_id
    }
    
        

@user_router_protected.get("/comments/me", response_model= List[GetComments])
def get_my_comments(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.state.auth_data["userID"]

    comments = db.query(models.Comment).filter(
        models.Comment.commenter_id == user_id
    ).all()

    return comments

@user_router_protected.get("/posts/me", response_model=List[PostGetUser])
def get_my_post(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.state.auth_data["userID"]
    

    posts = db.query(
    models.Posts,
    exists().where(
        and_(
            models.Like.post_id == models.Posts.id,
            models.Like.user_id == user_id
        )
    ).label("isLiked")
).filter(
    models.Posts.user_id == user_id
).options(joinedload(models.Posts.user)).all()

    result = []
    for post, is_liked in posts:
        post_dict = post.__dict__.copy()
        post_dict.pop("_sa_instance_state", None)
        post_dict["isLiked"] = is_liked
        result.append(post_dict)

    return result