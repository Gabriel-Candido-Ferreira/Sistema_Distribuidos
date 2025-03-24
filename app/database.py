import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "meu_banco")

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

def get_database():
    return database