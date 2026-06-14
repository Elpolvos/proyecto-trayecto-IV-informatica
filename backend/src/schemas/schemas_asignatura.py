from pydantic import BaseModel, Field
from datetime import time

class AsignaturaBase(BaseModel):
    fk_usuario_id: int
    fk_seccion_id: int
    nombre_asignatura: str
    contenido_asignatura: str | None = None
    hora_inicio: time
    hora_fin: time

class Asignatura(AsignaturaBase):
    id_asignatura: int

    class Config:
        from_attributes = True

class AsignaturaCreate(AsignaturaBase):
    pass

class AsignaturaEstatus(BaseModel):
    estatus_asignatura: bool = Field(default=True)

class AsignaturaEstatusUpdate(AsignaturaEstatus):
    pass