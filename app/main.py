from fastapi import FastAPI
from routers.posts import post_router
from routers.users import user_router
from services.database import engine
from entities.models import Base


app= FastAPI()

@app.get("/")
async def root():
    return {"message":"elle"}

Base.metadata.create_all(engine)

app.include_router(post_router)
app.include_router(user_router)

