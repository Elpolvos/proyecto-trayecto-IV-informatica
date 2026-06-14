from pydantic import BaseModel, Field

class AprobacionBase(BaseModel):
    estado_aprobacion: str

class Aprobacion(AprobacionBase):
    id_estado_aprobacion: int

    class Config:
        from_attributes = True

class AprobacionCreate(AprobacionBase):
    pass

class AprobacionEstatus(BaseModel):
    estatus_aprobacion: bool = Field(default=True)

class AprobacionEstatusUpdate(AprobacionEstatus):
    pass