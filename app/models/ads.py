from pydantic import BaseModel, validator,ConfigDict
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone
from app.models.states import States
from app.models.collection import Collection
from app.models.user import User
# from user import User

class Ads(BaseModel):
    image: object
    iduser: str 
    status: bool
    date_created: datetime
    title: str
    category: Collection
    price: float
    description: Optional[str] = None
    price_negotiable: bool
    views: int
    state: States

    @classmethod
    def from_mongo(cls, data):
        """Converte os dados do MongoDB para um formato adequado ao Pydantic"""
        if data and '_id' in data:
            data['id'] = str(data['_id'])
            del data['_id']
        return cls(**data)

    @validator('title')
    def validate_title(cls, v):
        if len(v) < 5:
            raise ValueError('O título deve ter pelo menos 5 caracteres')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('O preço deve ser um valor positivo')
        return v

    @validator('price_negotiable')
    def validate_price_negotiable(cls, v):
        if not isinstance(v, bool):
            raise ValueError('price_negotiable deve ser um valor booleano (True/False)')
        return v

    @validator('views')
    def validate_views(cls, v):
        if v < 0:
            raise ValueError('O número de visualizações não pode ser negativo')
        return v

    @validator('date_created')
    def validate_date_created(cls, v):
        if v.tzinfo is None: 
            v = v.replace(tzinfo=timezone.utc)
        
        if v > datetime.now(timezone.utc):
            raise ValueError('A data de criação não pode ser no futuro')
        
        return v
