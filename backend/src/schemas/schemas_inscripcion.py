from pydantic import BaseModel, Field
from datetime import date

class InscripcionBase(BaseModel):
    fk_usuario_id: int
    fk_seccion_id: int
    fecha_inscripcion: date
    anio_escolar: int

class Inscripcion(InscripcionBase):
    id_inscripcion: int

    class Config:
        from_attributes = True

class InscripcionCreate(InscripcionBase):
    pass

class InscripcionEstatus(BaseModel):
    estatus_inscripcion: bool = Field(default=True)

class InscripcionEstatusUpdate(InscripcionEstatus):
    pass