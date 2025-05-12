from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from app.database import db
from pydantic import BaseModel, ValidationError
from app.schemas.schema_portao import Portao

portoes_collection = db.portoes

def portao_helper(portao) -> dict:
    return {
        "id": str(portao["_id"]),  
        "codigo": portao["codigo"],
        "disponivel": portao["disponivel"],
    }

async def criar_indice():
    await portoes_collection.create_index([("codigo", 1)], unique=True)

async def listar_portoes():
    portoes = []
    async for portao in portoes_collection.find():
        portoes.append(portao_helper(portao))
    return portoes

async def criar_portao(data: dict):
    try:
        portao_data = Portao(**data)
    except ValidationError as e:
        raise ValueError(f"Erro de validação: {e.errors()}")

    codigo_existente = await portoes_collection.find_one({"codigo": portao_data.codigo})
    if codigo_existente:
        raise ValueError(f"O código {portao_data.codigo} já está em uso.")

    try:
        portao_data_dict = portao_data.dict()
        result = await portoes_collection.insert_one(portao_data_dict)
        portao = await portoes_collection.find_one({"_id": result.inserted_id})
        return portao_helper(portao)
    except DuplicateKeyError:
        raise ValueError(f"O código {portao_data.codigo} já existe.")

async def buscar_portao(id: str):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise ValueError("ID inválido.")
    
    portao = await portoes_collection.find_one({"_id": obj_id})
    if portao:
        return portao_helper(portao)
    
async def atualizar_portao(id: str, data: dict):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise ValueError("ID inválido.")
    
    await portoes_collection.update_one({"_id": obj_id}, {"$set": data})
    return await buscar_portao(id)


async def deletar_portao(id: str):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise ValueError("ID inválido.")
    
    resultado = await portoes_collection.delete_one({"_id": obj_id})
    return resultado.deleted_count > 0
