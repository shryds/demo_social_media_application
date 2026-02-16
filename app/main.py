from fastapi import FastAPI
from app.routers.posts import post_router
from app.routers.users import user_router, user_router_protected
from app.services.database import engine
from app.entities.models import Base


app= FastAPI()

@app.get("/")
async def root():
    return {"message":"elle"}

Base.metadata.create_all(engine)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(user_router_protected)



