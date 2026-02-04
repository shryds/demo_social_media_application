from fastapi import APIRouter

post_router=APIRouter()

@post_router.get("/posts")
async def get_posts():
    return {"message":"this is ur post"}


