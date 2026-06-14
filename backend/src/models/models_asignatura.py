from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, Time, Table, Text, Numeric, DECIMAL
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from datetime import datetime

class Asignaturas(Base):
    id_asignatura = Column(Integer, primary_key=True, index=True)
    fk_usuario_id = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fk_seccion_id = Column(Integer, ForeignKey('secciones.id_seccion'), nullable=False)
    nombre_asignatura = Column(String(100), unique=True, nullable=False)
    contenido_asignatura = Column(String(500))
    hora_inicio = Column (Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estatus_asignatura = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    usuario = relationship('Usuarios', back_populates='asignatura')
    seccion = relationship('Secciones', back_populates='asignatura')
    evaluacion = relationship('Evaluaciones', back_populates='asignatura')
    asistencia = relationship("Asistencias", back_populates="asignatura")
    nota_final = relationship("Notas_Finales", back_populates="asignatura")