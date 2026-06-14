from pydantic import BaseModel, Field
from datetime import date

class TrimestreBase(BaseModel):
    nombre_trimestre: str
    fecha_inicio: date
    fecha_fin: date

class Trimestre(TrimestreBase):
    id_trimestre: int

    class Config:
        from_attributes = True

class TrimestreCreate(TrimestreBase):
    pass

class TrimestreEstatus(BaseModel):
    estatus_trimestre: bool = Field(default=True)

class TrimestreEstatusUpdate(TrimestreEstatus):
    pass