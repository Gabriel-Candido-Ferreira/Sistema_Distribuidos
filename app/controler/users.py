from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.models.user import User
from bson import ObjectId

router = APIRouter()

@router.post("/users/")
async def create_user(user: User, database: AsyncIOMotorDatabase = Depends(get_database)):
    user_dict = user.dict()
    try:
        result = await database["users"].insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)  
        return user_dict  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o usuário: {str(e)}")
    
@router.get("/users/", response_model=list[User])
async def get_users(database: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        users = await database["users"].find().to_list(length=None)  
        for user in users:
            user["_id"] = str(user["_id"])
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar usuários: {str(e)}")

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, database: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        user = await database["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar usuário: {str(e)}")

