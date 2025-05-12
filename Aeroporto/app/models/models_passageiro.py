from fastapi import HTTPException
from app.database import db
from app.schemas.schema_passageiro import Passageiro
import uuid

passageiros_collection = db.passageiros

def passageiro_helper(passageiro) -> dict:
    return {
        "id": str(passageiro["_id"]),  
        "nome": passageiro["nome"],
        "cpf": passageiro["cpf"],
        "vooId": passageiro["vooId"],
        "statusCheckIn": passageiro["statusCheckIn"]
    }

async def criar_passageiro(passageiro_data: Passageiro):
    passageiro_existente = await passageiros_collection.find_one({"cpf": passageiro_data.cpf})
    if passageiro_existente:
        raise HTTPException(status_code=400, detail="Passageiro com este CPF já existe.")
    
    passageiro_dict = passageiro_data.dict()
    await passageiros_collection.insert_one(passageiro_dict)
    return {"message": "Passageiro criado com sucesso!"}

async def obter_todos_passageiros():
    passageiros_cursor = passageiros_collection.find()
    passageiros = []
    async for passageiro in passageiros_cursor:
        passageiros.append(passageiro_helper(passageiro))
    return passageiros

async def buscar_passageiro(id: str):
    passageiro = await passageiros_collection.find_one({"_id": id})
    if passageiro:
        return passageiro_helper(passageiro)

async def atualizar_passageiro(id: str, data: dict):
    await passageiros_collection.update_one({"_id": id}, {"$set": data})
    return await buscar_passageiro(id)

async def deletar_passageiro(id: str):
    resultado = await passageiros_collection.delete_one({"_id": id})
    return resultado.deleted_count > 0
