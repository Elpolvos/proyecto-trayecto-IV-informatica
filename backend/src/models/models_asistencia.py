from sqlalchemy import Boolean, Column, UniqueConstraint, Integer, ForeignKey, String, Date, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Asistencias(Base):
    id_asistencia = Column(Integer, primary_key=True, index=True)
    fk_usuario_id = Column(Integer,ForeignKey('usuarios.id_usuario'), nullable=False)
    fk_asignatura_id = Column(Integer,ForeignKey('asignaturas.id_asignatura'), nullable=False)
    fecha_asistencia = Column(Date, nullable=False)
    presente = Column(Boolean, default=True)
    estatus_asistencia = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    usuario = relationship('Usuarios', back_populates='asistencia')
    asignatura = relationship("Asignaturas", back_populates="asistencia")

    __table_args__ = (
        UniqueConstraint('fk_usuario_id', 'fk_asignatura_id', 'fecha_asistencia',
                        name='unique_asistencia_diaria'),
    )