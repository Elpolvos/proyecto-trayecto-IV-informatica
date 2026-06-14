from pydantic import BaseModel, Field

class NotaFinalBase(BaseModel):
    fk_usuario_id: int
    fk_asignatura_id: int
    fk_trimestre_id: int
    nota_promedio: float
    porcentaje_asistencia: float
    estado_aprobacion: str

class NotaFinal(NotaFinalBase):
    id_nota_final: int

    class Config:
        from_attributes = True

class NotaFinalCreate(NotaFinalBase):
    pass

class NotaFinalEstatus(BaseModel):
    estatus_nota_final: bool = Field(default=True)

class NotaFinalEstatusUpdate(NotaFinalEstatus):
    pass

class NotaFinalPromedio(BaseModel):
    nota_promedio: float
    estado_aprobacion: str

class NotaFinalPromedioUpdate(NotaFinalPromedio):
    pass