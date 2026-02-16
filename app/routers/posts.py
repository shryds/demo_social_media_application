from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.entities import models
from app.services.database import get_db
from app.entities.schemas import PostCreate, PostGet
from sqlalchemy.orm import Session

post_router=APIRouter(prefix="/post")

@post_router.get("/all", response_model= List[PostGet])
async def get_posts(db: Session=Depends(get_db)):
    items= db.query(models.Posts).all()
    return items

@post_router.post("/" ,status_code=HTTPStatus.CREATED)
async def create_post(new_post:PostCreate,db: Session=Depends(get_db)):
    post= models.Posts(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return None

@post_router.get("/{id}", response_model= PostGet)
async def get_post(id:int,db: Session=Depends(get_db)):
    stmt = select(models.Posts).filter(models.Posts.id == id)
    post = db.scalar(stmt)
    return post
