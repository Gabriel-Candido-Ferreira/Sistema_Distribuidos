from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
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
        if v > datetime.now():
            raise ValueError('A data de criação não pode ser no futuro')
        return v
