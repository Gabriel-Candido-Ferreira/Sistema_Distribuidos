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
    
@router.put("/collection/{collection_id}")
async def update_collection(collection_id: str, collection: Collection, database: AsyncIOMotorDatabase = Depends(get_database)):
    collection_dict = collection.dict(exclude={"id"})
    try:
        result = await database["collections"].update_one(
            {"_id": ObjectId(collection_id)}, 
            {"$set": collection_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Coleção não encontrado")
        
        return {"message": "Coleção atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar a Colção: {str(e)}")
    
@router.get("/collection/", response_model=list[Collection])
async def get_collections(database: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        collections = await database["collection"].find().to_list(length=None)  
        for collection in collections:
            collection["_id"] = str(collection["_id"])
        return collections
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar uma collection: {str(e)}")