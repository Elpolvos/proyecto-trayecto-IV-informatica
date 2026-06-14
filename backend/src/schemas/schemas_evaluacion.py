from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date

class EvaluacionBase(BaseModel):
    fk_asignatura_id: int
    fk_trimestre_id: int

    numero_evaluacion: str
    descripcion_evaluacion: str | None = None
    porcentaje_evaluacion: Decimal
    puntuacion_nota: int
    acumulativo: float

    fecha_registro: date


class Evaluacion(EvaluacionBase):
    id_evaluacion: int

    class Config:
        from_attributes = True

class EvaluacionCreate(EvaluacionBase):
    pass

class EvaluacionEstatus(BaseModel):
    estatus_evaluacion: bool = Field(default=True)

class EvaluacionEstatusUpdate(EvaluacionEstatus):
    pass