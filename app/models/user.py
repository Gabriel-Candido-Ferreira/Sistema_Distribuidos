from pydantic import BaseModel, EmailStr, validator
from app.models.states import States
from app.models.collection import Collection
from app.models.ads import Ads

class User(BaseModel):
    name: str
    name_slug: str
    email: EmailStr
    state: States
    passwordHash: str
    token: str
    Collection: Collection
    ads: Ads

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('O nome deve ter pelo menos 3 caracteres')
        return v

    @validator('name_slug')
    def validate_name_slug(cls, v):
        if len(v) < 3:
            raise ValueError('O name slug deve ter pelo menos 3 caracteres')
        return v
    
    @validator('passwordHash')
    def validate_password_hash(cls, v):
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres no hash')
        return v

    @validator('token')
    def validate_token(cls, v):
        if not v:
            raise ValueError('O token não pode estar vazio')
        return v