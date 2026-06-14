from pydantic import BaseModel, Field

class SeccionBase(BaseModel):
    descripcion_seccion: str

class Seccion(SeccionBase):
    id_seccion: int

    class Config:
        from_attributes = True

class SeccionCreate(SeccionBase):
    pass

class SeccionEstatus(BaseModel):
    estatus_seccion: bool = Field(default=True)

class SeccionEstatusUpdate(SeccionEstatus):
    pass