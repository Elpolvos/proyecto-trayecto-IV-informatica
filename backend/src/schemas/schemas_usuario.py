from pydantic import BaseModel, Field
from datetime import date

class UsuarioBase(BaseModel):
    fk_rol_id: int
    dni_usuario: str
    apellido_usuario: str
    nombre_usuario: str
    fechanacimiento_usuario: date
    sexo_usuario: str
    direccion_usuario: str
    telefono_usuario: str
    email_usuario: str
    contrasena_usuario : str

    fecha_registro: date

class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioEstatus(BaseModel):
    estatus_usuario: bool = Field(default=True)

class UsuarioEstatusUpdate(UsuarioEstatus):
    pass