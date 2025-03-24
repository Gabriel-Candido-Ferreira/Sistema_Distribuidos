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