from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.models.user import User
from pydantic import BaseModel
from bson import ObjectId
from app.utils.security import hash_password

router = APIRouter()

@router.post("/users/")
async def create_user(user: User, database: AsyncIOMotorDatabase = Depends(get_database)):
    user_dict = user.dict()

    # Aplica o hash na senha
    user_dict["password"] = hash_password(user_dict["password"])

    try:
        result = await database["users"].insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o usuário: {str(e)}")
    
@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User, database: AsyncIOMotorDatabase = Depends(get_database)):
    user_dict = user.dict()

    # Verifica se o estado existe
    existing_state = await database["states"].find_one({"_id": ObjectId(user.state.id)})
    if not existing_state:
        raise HTTPException(status_code=400, detail="Estado informado não existe")

    # Verifica duplicidade de e-mail
    existing_user = await database["users"].find_one({"email": user.email, "_id": {"$ne": ObjectId(user_id)}})
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado para outro usuário")

    # Re-hash da senha
    user_dict["password"] = hash_password(user_dict["password"])

    result = await database["users"].update_one(
        {"_id": ObjectId(user_id)}, 
        {"$set": user_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"message": "Usuário atualizado com sucesso"}
    
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

