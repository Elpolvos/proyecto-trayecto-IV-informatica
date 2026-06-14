from sqlalchemy import Boolean, Column, Integer, Date, ForeignKey, String, DateTime, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Trimestres(Base):
    id_trimestre = Column(Integer, primary_key=True, index=True)
    nombre_trimestre = Column(String(100), nullable=False)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estatus_trimestre = Column(Boolean, default=True, server_default="true")

    # RELACIONES

    evaluacion = relationship("Evaluaciones", back_populates="trimestre")
    nota_final = relationship("Notas_Finales", back_populates="trimestre")