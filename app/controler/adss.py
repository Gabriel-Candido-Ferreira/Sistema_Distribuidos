from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database
from app.models.ads import Ads
from bson import ObjectId

router = APIRouter()

@router.post("/ads/")
async def create_ads(ads: Ads, database: AsyncIOMotorDatabase = Depends(get_database)):
    ads_dict = ads.dict()
    try:
        result = await database["ads"].insert_one(ads_dict)
        ads_dict["_id"] = str(result.inserted_id)  
        return ads_dict  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar um collection: {str(e)}")
    
@router.get("/ads/", response_model=list[Ads])
async def get_adss(database: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        adss = await database["ads"].find().to_list(length=None)  
        for ads in adss:
            ads["_id"] = str(ads["_id"])
        return adss
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar uma collection: {str(e)}")
    
@router.put("/ads/{ads_id}")
async def update_ads(ads_id: str, ads: Ads, database: AsyncIOMotorDatabase = Depends(get_database)):
    ads_dict = ads.dict(exclude={"id", "data_de_criacao", "views"})
    try:
        result = await database["adsrs"].update_one(
            {"_id": ObjectId(ads_id)}, 
            {"$set": ads_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Anuncio não encontrado")
        
        return {"message": "Anuncio atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar o Anuncio: {str(e)}")
    
@router.delete("/ads/{ads_id}", response_model=Ads)
async def delete_ads(ads_id: str, database: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        ads = await database["adss"].find_one({"_id": ObjectId(ads_id)})
        if ads:
            await database["adss"].delete_one({"_id": ObjectId(ads_id)})
            ads["_id"] = str(ads["_id"])  
            return ads
        raise HTTPException(status_code=404, detail="ads não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar ads: {str(e)}")