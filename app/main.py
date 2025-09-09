# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection
from routes import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await connect_to_mongo()
    yield
    
    await close_mongo_connection()

app = FastAPI(
    lifespan=lifespan,
    title="User Management API",
    description="API for managing users with FastAPI and MongoDB",
    version="1.0.0"
)


app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the User Management API!"}