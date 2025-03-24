from pydantic import BaseModel, validator

class States(BaseModel):
    name: str

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError('O nome deve ter pelo menos 3 caracteres')
        return v