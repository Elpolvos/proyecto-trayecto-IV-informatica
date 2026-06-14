from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base

class Roles(Base):
    id_rol = Column(Integer, primary_key=True, index=True)
    tipo_rol = Column(String(100), nullable=False)
    estatus_rol = Column(Boolean, default=True, server_default="true")
    
    #RELACIONES

    usuario = relationship('Usuarios', back_populates='rol')