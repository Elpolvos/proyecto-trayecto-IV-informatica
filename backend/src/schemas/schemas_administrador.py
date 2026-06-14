from pydantic import BaseModel, Field
from datetime import date

class AdministradorBase(BaseModel):
    dni_administrador : str
    apellido_administrador : str
    nombre_administrador : str
    fechanacimiento_administrador : date
    sexo_administrador : str
    direccion_administrador : str
    telefono_administrador : str
    email_administrador: str
    contrasena_administrador : str

class Administrador(AdministradorBase):
    id_administrador : int

    class Config:
        from_attributes = True

class AdministradorCreate(AdministradorBase):
    pass

class AdministradorEstatus(BaseModel):
    estatus_administrador : bool = Field(default = True)

class AdministradorEstatusUpdate(AdministradorEstatus):
    pass