from pydantic import BaseModel, Field
from datetime import datetime

class NotaBase(BaseModel):
    id_evaluacion: int
    id_estudiante: int
    puntuacion_nota: int
    fecha_registro: datetime

class Nota(NotaBase):
    id_nota: int

    class Config:
        from_attributes = True

class NotaCreate(NotaBase):
    pass

class NotaEstatus(BaseModel):
    estatus_nota: bool = Field(default=True)

class NotaEstatusUpdate(NotaEstatus):
    pass

class NotaPuntuacion(BaseModel):
    puntuacion_nota: int

class NotaPuntuacionUpdate(NotaPuntuacion):
    pass