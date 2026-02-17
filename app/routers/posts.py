from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from app.entities import models
from app.middlewares.auth import auth_middleware
from app.services.database import get_db
from app.entities.schemas import PostCreate, PostGet
from sqlalchemy.orm import Session

post_router=APIRouter(prefix="/post")

post_router_protected = APIRouter(
    prefix="/post",
    tags=["protected"],dependencies=[Depends(auth_middleware)],
)

@post_router.get("/all", response_model= List[PostGet])
async def get_posts(db: Session=Depends(get_db)):
    items= db.query(models.Posts).all()
    return items

@post_router_protected.post("/" ,status_code=HTTPStatus.CREATED)
async def create_post(new_post:PostCreate,request:Request, db: Session=Depends(get_db)):
    user_id=request.state.auth_data["userID"]
    #if not user_id:
        #raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="token issue")
    post= models.Posts(**new_post.dict())
    post.user_id = user_id
    db.add(post)
    db.commit()
    db.refresh(post)
    return None

@post_router.get("/{id}", response_model=PostGet)
async def get_post(id:int,db: Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    return post
