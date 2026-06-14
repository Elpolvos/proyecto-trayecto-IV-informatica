from pydantic import BaseModel, Field

class RolBase(BaseModel):
    tipo_rol: str

class Rol(RolBase):
    id_rol: int

    class Config:
        from_attributes = True

class RolCreate(RolBase):
    pass

class RolEstatus(BaseModel):
    estatus_rol: bool = Field(default=True)

class RolEstatusUpdate(RolEstatus):
    pass