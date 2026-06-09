from fastapi import FastAPI
from app.routers.posts import post_router,post_router_protected
from app.routers.users import user_router, user_router_protected
from app.services.database import engine
from app.entities.models import Base
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

origins = [
    "http://localhost:5173",
    "https://demo-social-media-ui.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,       
    allow_methods=["*"],         
    allow_headers=["*"],           
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}

Base.metadata.create_all(engine)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(user_router_protected)
app.include_router(post_router_protected)




