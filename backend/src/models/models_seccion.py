from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Secciones(Base):
    id_seccion = Column(Integer, primary_key=True, index=True)
    descripcion_seccion = Column(String(100), nullable=False)
    estatus_seccion = Column(Boolean, default=True, server_default="true")
    
    #RELACIONES

    asignatura = relationship('Asignaturas', back_populates='seccion')
    inscripcion = relationship('Inscripciones', back_populates='seccion')