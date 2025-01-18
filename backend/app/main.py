from fastapi import FastAPI
from app.routes import users, conversations, documents
from app.middleware import setup_middleware
from app.db import init as init_db

app = FastAPI(title="My Backend API")

setup_middleware(app)
app.include_router(conversations.router)
app.include_router(users.router)
app.include_router(documents.router)

@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie

@app.get("/")
def read_root():
    return {"message": "Welcome to my Backend API!"}