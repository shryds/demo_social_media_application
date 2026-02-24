from http import HTTPStatus
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request,UploadFile,File
from sqlalchemy import delete, select
from app.entities import models
from app.middlewares.auth import auth_middleware
from app.services.database import get_db
from app.entities.schemas import CommentCreate, GetComments, PostCreate, PostGet
from sqlalchemy.orm import Session

from app.services.image import store_file

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
async def create_post(
    title:Annotated[str, Form()],
    content:Annotated[str, Form()],
    request:Request, 
    file:Optional[UploadFile] = None ,
    db: Session=Depends(get_db)
):
    user_id=request.state.auth_data["userID"]
    #if not user_id:
        #raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="token issue")
    
    new_post={
        "title":title,
        "content":content,
        "img_path":await store_file(file),
        "user_id":user_id
    }
    # new_post.content=content
    # new_post.title=title
    post= models.Posts(**new_post)
    db.add(post)
    db.commit()
    db.refresh(post)
    return None

@post_router.get("/{id}", response_model=PostGet)
async def get_post(id:int,db: Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    return post

@post_router_protected.patch("/{id}",response_model=PostCreate)
async def update_post(new_post_info:PostCreate, id:int,request: Request,db: Session=Depends(get_db)):
    auth_id=request.state.auth_data["userID"]
    post = db.query(models.Posts).filter(models.Posts.id==id).first()

    if(auth_id!=post.user_id):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    db.query(models.Posts).filter(models.Posts.id==id).update({"title":new_post_info.title,"content":new_post_info.content})
    db.commit()
    return post

@post_router_protected.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_post(id:int,request: Request,db: Session=Depends(get_db)):
    auth_id=request.state.auth_data["userID"]
    post = db.query(models.Posts).filter(models.Posts.id==id).first()

    if(auth_id!=post.user_id):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    stmt=delete(models.Posts).where(models.Posts.id==id)
    db.execute(stmt)
    db.commit()
    return None

@post_router_protected.post("/{id}/like",status_code=HTTPStatus.NO_CONTENT)
async def liked_post(id:int, request:Request,db:Session=Depends(get_db)):
    auth_id=request.state.auth_data["userID"]
    post_by_id = db.query(models.Posts).filter(models.Posts.id==id)
    post_res = post_by_id.first()
    if not post_res:
        raise HTTPStatus.BAD_REQUEST
    
    like={"post_id":id,"user_id":auth_id}
    like_model=models.Like(**like)
    db.add(like_model)
    post_by_id.update({"likes":models.Posts.likes+1})
    db.commit()
    return None

@post_router_protected.delete("/{id}/like",status_code=HTTPStatus.NO_CONTENT)
async def delete_like(id:int,request:Request,db:Session=Depends(get_db)):
    # auth
        # get auth user id
        # get like by post_id and user_id
        # if like is None raise exepction
    # updation
        # delete like row
        # decrement post.likes
    
    auth_id=request.state.auth_data["userID"]
    post_by_id = db.query(models.Posts).filter(models.Posts.id==id)
    like=db.query(models.Like).filter(models.Like.user_id==auth_id and models.Like.post_id==id).first()

    if not like:
        raise HTTPStatus.BAD_REQUEST
    
    stmt=delete(models.Like).where(models.Like.post_id==id and models.Like.user_id==auth_id)
    db.execute(stmt)
    post_by_id.update({"likes":models.Posts.likes-1})
    db.commit()
    return None

@post_router.get("/{id}/likes")
async def all_likes(id: int, db:Session=Depends(get_db)):
    likes=db.query(models.Like).filter(models.Like.post_id==id).all()

    return [row.user_id for row in likes]

@post_router_protected.post("/{id}/comment")
async def post_comment(new_comment:CommentCreate,request:Request, id:int ,db:Session=Depends(get_db)):
    auth_user_id=request.state.auth_data["userID"]
    post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    comment= models.Comment(**new_comment.dict())
    comment.commenter_id = auth_user_id
    comment.post_id=post.id
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return None

@post_router.get("/{id}/comments/all", response_model= List[GetComments])
async def get_comments(id:int,db: Session=Depends(get_db)):
    post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if not post:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    items= db.query(models.Comment).filter(models.Comment.post_id==id).all()
    return items

@post_router_protected.delete("/comment/{id}")
async def delete_comment(id:int, request:Request,db:Session=Depends(get_db)):
    auth_user=request.state.auth_data["userID"]
    comment=db.query(models.Comment).filter(models.Comment.id==id).first()
    if not comment:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    post_id=comment.post_id
    post=db.query(models.Posts).filter(models.Posts.id==post_id).first()
    creator=post.user_id

    if auth_user!=comment.commenter_id and auth_user!=creator :
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    
    stmt=delete(models.Comment).where(models.Comment.id==id)
    db.execute(stmt)
    db.commit()
    return None

@post_router_protected.patch("/comment/{id}")
async def update_comment(updated_comment:CommentCreate,id:int,request:Request,db:Session=Depends(get_db)):
    auth_id=request.state.auth_data["userID"]
    comment=db.query(models.Comment).filter(models.Comment.id==id).first()
    if not comment:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    if auth_id!=comment.commenter_id:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
     
    db.query(models.Comment).filter(models.Comment.id==id).update({"comment":updated_comment.comment})
    db.commit()
    return updated_comment