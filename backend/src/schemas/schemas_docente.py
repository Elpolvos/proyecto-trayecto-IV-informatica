from pydantic import BaseModel, Field
from datetime import date

class DocenteBase(BaseModel):
    dni_docente: str
    apellido_docente: str
    nombre_docente: str
    fechanacimiento_docente: date
    sexo_docente: str
    direccion_docente: str
    telefono_docente: str
    email_docente: str
    contrasena_docente : str


class Docente(DocenteBase):
    id_docente: int

    class Config:
        from_attributes = True

class DocenteCreate(DocenteBase):
    pass

class DocenteEstatus(BaseModel):
    estatus_docente: bool = Field(default=True)

class DocenteEstatusUpdate(DocenteEstatus):
    pass