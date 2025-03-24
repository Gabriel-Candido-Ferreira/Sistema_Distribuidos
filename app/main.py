# app/main.py
from enum import Enum
import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.controler import users, collections, adss

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "meu_banco")

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["users"])

app.include_router(collections.router, prefix="/api", tags=["collections"])

app.include_router(adss.router, prefix="/api", tags=["adss"])


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000)))
