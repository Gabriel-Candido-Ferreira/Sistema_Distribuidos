from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.models.collection import Collection
from bson import ObjectId

router = APIRouter()

@router.post("/collection/")
async def create_collection(collection: Collection, database: AsyncIOMotorDatabase = Depends(get_database)):
    collection_dict = collection.dict()
    try:
        result = await database["collection"].insert_one(collection_dict)
        collection_dict["_id"] = str(result.inserted_id)  
        return collection_dict  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar um collection: {str(e)}")
    
@router.get("/collection/", response_model=list[Collection])
async def get_collections(database: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        collections = await database["collection"].find().to_list(length=None)  
        for collection in collections:
            collection["_id"] = str(collection["_id"])
        return collections
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar uma collection: {str(e)}")