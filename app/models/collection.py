from pydantic import BaseModel, validator

class Collection(BaseModel):
    name: str
    slug: str

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('O nome deve ter pelo menos 3 caracteres')
        return v