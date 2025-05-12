from motor.motor_asyncio import AsyncIOMotorClient

# Criação da conexão assíncrona com o MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.aeroporto

# Definindo as coleções
passageiros_collection = db.get_collection("passageiros")
voos_collection = db.voos
portoes_collection = db.portoes
