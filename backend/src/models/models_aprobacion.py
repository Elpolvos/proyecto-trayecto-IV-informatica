from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base

class Estados_Aprobaciones(Base):
    id_estado_aprobacion = Column(Integer, primary_key=True, index=True)
    estado_aprobacion = Column(String(100), nullable=False) # Aprobado, Reprobado, Aplazado
    estatus_aprobacion = Column(Boolean, default=True, server_default="true")
    
    #RELACIONES

    nota_final = relationship('Notas_Finales', back_populates='aprobacion')