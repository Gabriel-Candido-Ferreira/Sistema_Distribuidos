from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.models.states import States
from bson import ObjectId

router = APIRouter()

@router.post("/states/")
async def create_states(collection: States, database: AsyncIOMotorDatabase = Depends(get_database)):
    states_dict = collection.dict()
    try:
        result = await database["states"].insert_one(states_dict)
        states_dict["_id"] = str(result.inserted_id)  
        return states_dict  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar um collection: {str(e)}")