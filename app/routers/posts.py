from http import HTTPStatus
from typing import List
from fastapi import APIRouter
from sqlalchemy import select
from entities import models
from services.database import get_db
from entities.schemas import PostCreate, PostGet

post_router=APIRouter()

@post_router.get("/posts", response_model= List[PostGet])
async def get_posts():
    db=get_db()
    items= db.query(models.Posts).all()
    return items

@post_router.post("/post" ,status_code=HTTPStatus.CREATED)
async def create_post(new_post:PostCreate):
    db=get_db()
    post= models.Posts(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return None



@post_router.get("/posts/{id}", response_model= PostGet)
async def get_post(id:int):
    db=get_db()
    stmt = select(models.Posts).filter(models.Posts.id == id)
    post = db.scalar(stmt)
    return post
