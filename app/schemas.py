from pydantic import BaseModel

class EmissionBase(BaseModel):
    country_name: str
    territorial_approach: float
    territorial_approach_by_inhabitant: float
    consumption_approach: float

class EmissionCreate(EmissionBase):
    pass

class Emission(EmissionBase):
    id: int

    class Config:
        orm_mode = True
