from pydantic import BaseModel, Field
from datetime import date

class AsistenciaBase(BaseModel):
    fk_usuario_id: int
    fk_asignatura_id: int
    fecha_asistencia: date
    presente: bool = Field(default=True)

class Asistencia(AsistenciaBase):
    id_asistencia: int

    class Config:
        from_attributes = True

class AsistenciaCreate(AsistenciaBase):
    pass

class AsistenciaEstatus(BaseModel):
    estatus_asistencia: bool = Field(default=True)

class AsistenciaEstatusUpdate(AsistenciaEstatus):
    pass

class AsistenciaPresente(BaseModel):
    presente: bool

class AsistenciaPresenteUpdate(AsistenciaPresente):
    pass