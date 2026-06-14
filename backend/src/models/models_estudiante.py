from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base

class Estudiantes(Base):
    id_estudiante = Column(Integer, primary_key=True, index=True)
    dni_estudiante = Column(String(8), unique=True, nullable=False, index=True)
    apellido_estudiante = Column(String(100), nullable=False)
    nombre_estudiante = Column(String(100), nullable=False)
    fechanacimiento_estudiante = Column(Date, nullable=False)
    sexo_estudiante = Column(String(10), nullable=False)
    direccion_estudiante = Column(String(255), nullable=False)
    telefono_estudiante = Column(String(20), nullable=False, unique=True)
    email_estudiante = Column(String(100), nullable=False, unique=True)
    contrasena_estudiante = Column (String(255), nullable=False, unique=True)
    estatus_estudiante = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    #nota = relationship('Notas', back_populates='estudiante')
    #inscripcion = relationship('Inscripciones', back_populates='estudiante')
    #asistencia = relationship('Asistencias', back_populates='estudiante')
    #nota_final = relationship('Notas_Finales', back_populates='estudiante')