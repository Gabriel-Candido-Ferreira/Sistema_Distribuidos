from pydantic import BaseModel, validator

class States(BaseModel):
    name: str

    @validator('name')
    def validate_name(cls, v):
        valid_states = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        if v.upper() not in valid_states:
            raise ValueError('Estado inválido')
        return v.upper()