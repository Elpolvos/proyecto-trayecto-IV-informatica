from sqlalchemy import Boolean, Column, UniqueConstraint, func, Integer, ForeignKey, String, DateTime, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Notas(Base):
    id_nota = Column(Integer, primary_key=True, index=True)
    fk_evaluacion_id = Column(Integer, ForeignKey('evaluaciones.id_evaluacion'), nullable=False)
    fk_estudiante_id = Column(Integer, ForeignKey('estudiantes.id_estudiante'), nullable=False)
    puntuacion_nota = Column(Integer, nullable=False)
    fecha_registro = Column(DateTime, default=func.now())
    estatus_nota = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    evaluacion = relationship("Evaluaciones", back_populates="nota")
    estudiante = relationship("Estudiantes", back_populates="nota")
    
    __table_args__ = (
        UniqueConstraint('fk_evaluacion_id', 'fk_estudiante_id', 
                        name='unique_nota_estudiante_evaluacion'),
    )