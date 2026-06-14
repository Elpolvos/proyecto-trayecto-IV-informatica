from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Table, Text, Numeric, DECIMAL, func, Float
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Evaluaciones(Base):
    id_evaluacion = Column(Integer, primary_key=True, index=True)
    
    fk_asignatura_id = Column(Integer, ForeignKey('asignaturas.id_asignatura'), nullable=False)
    fk_trimestre_id = Column(Integer, ForeignKey("trimestres.id_trimestre"), nullable=False)
    
    numero_evaluacion = Column(String(2), nullable=False)
    descripcion_evaluacion = Column(String(100), nullable=False)
    porcentaje_evaluacion = Column(Numeric(scale=2), nullable=False)
    puntuacion_nota = Column(Integer, nullable=False)
    acumulativo = Column (Float, nullable=False)
    
    fecha_registro = Column(DateTime, default=func.now())
    estatus_evaluacion = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    asignatura = relationship('Asignaturas', back_populates='evaluacion')
    trimestre = relationship("Trimestres", back_populates="evaluacion")