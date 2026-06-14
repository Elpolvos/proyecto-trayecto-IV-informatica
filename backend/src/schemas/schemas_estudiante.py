from pydantic import BaseModel, Field
from datetime import date

class EstudianteBase(BaseModel):
    dni_estudiante: str
    apellido_estudiante: str
    nombre_estudiante: str
    fechanacimiento_estudiante: date
    sexo_estudiante: str
    direccion_estudiante: str
    telefono_estudiante: str
    email_estudiante: str
    contrasena_estudiante : str

class Estudiante(EstudianteBase):
    id_estudiante: int

    class Config:
        from_attributes = True

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteEstatus(BaseModel):
    estatus_estudiante: bool = Field(default=True)

class EstudianteEstatusUpdate(EstudianteEstatus):
    pass