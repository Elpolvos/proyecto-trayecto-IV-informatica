from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, Date, func, Table, Text, Numeric, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Inscripciones(Base):
    id_inscripcion = Column(Integer, primary_key=True, index=True)
    fk_usuario_id = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fk_seccion_id = Column(Integer, ForeignKey('secciones.id_seccion'), nullable=False)
    fecha_inscripcion = Column(Date, default=func.current_date())
    anio_escolar = Column(String(20), nullable=False)
    estatus_inscripcion = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    usuario = relationship('Usuarios', back_populates='inscripcion')
    seccion = relationship("Secciones", back_populates="inscripcion")

    __table_args__ = (
        UniqueConstraint('fk_usuario_id', 'fk_seccion_id', 'anio_escolar', 
                        name='unique_inscripcion'),
    )