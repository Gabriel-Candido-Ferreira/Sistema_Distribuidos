from app.database import db
from app.models.models_portao import portoes_collection
from app.schemas.schema_voo import Voo
from fastapi import HTTPException
import uuid


voos_collection = db.voos

def voo_helper(voo) -> dict:
    return {
        "id": str(voo["_id"]), 
        "numeroVoo": voo["numeroVoo"],
        "origem": voo["origem"],
        "destino": voo["destino"],
        "dataHoraPartida": voo["dataHoraPartida"].isoformat() if "dataHoraPartida" in voo else None,
        "portaoId": str(voo["portaoId"]) if "portaoId" in voo else None,
        "status": voo["status"]
    }

async def criar_voo(voo_data: Voo):
    portao = await portoes_collection.find_one({"_id": voo_data.portaoId})
    if not portao or not portao["disponivel"]:
        raise HTTPException(status_code=400, detail="Portão não encontrado ou não disponível.")
    
    await portoes_collection.update_one(
        {"_id": voo_data.portaoId}, 
        {"$set": {"disponivel": False}}
    )
    
    await voos_collection.insert_one(voo_data.dict())
    return {"message": "Voo criado com sucesso!"}


async def obter_todos_voos():
    voos_cursor = voos_collection.find()  
    voos = []
    async for voo in voos_cursor:  
        voos.append(voo_helper(voo))
    return voos



async def obter_voo_por_id(voo_id: str):
    try:
        if not isinstance(voo_id, str):
            raise ValueError("ID deve ser uma string")
        
        voo_id_uuid = uuid.UUID(voo_id) 

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"ID inválido: {str(e)}")

    voo = await voos_collection.find_one({"_id": voo_id_uuid})
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")
    
    return voo_helper(voo)

async def atualizar_voo(voo_id: str, voo_data: Voo):
    voo = await voos_collection.find_one({"_id": voo_id})
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")
    
    await voos_collection.update_one({"_id": voo_id}, {"$set": voo_data.dict()})
    
    if voo_data.status == "concluído" and "portaoId" in voo_data:
        await portoes_collection.update_one(
            {"_id": voo_data.portaoId},
            {"$set": {"disponivel": True}}
        )
    
    return {"message": "Voo atualizado com sucesso!"}

async def deletar_voo(voo_id: str):
    if not await voos_collection.find_one({"_id": voo_id}):
        raise HTTPException(status_code=404, detail="Voo não encontrado.")
    
    await voos_collection.delete_one({"_id": voo_id})
    return {"message": "Voo deletado com sucesso!"}