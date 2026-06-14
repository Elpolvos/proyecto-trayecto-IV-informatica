from datetime import datetime
from sqlalchemy import String, Boolean, Column, Integer, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column

class Usuarios(Base):

    id_usuario = Column(Integer, primary_key=True, index=True)
    fk_rol_id = Column(Integer, ForeignKey('roles.id_rol'), nullable=False, index=True)
    dni_usuario = Column(String(20), unique=True, nullable=False, index=True)
    apellido_usuario = Column(String(100), nullable=False)
    nombre_usuario = Column(String(100), nullable=False)
    fechanacimiento_usuario = Column(DateTime, server_default=func.now())
    sexo_usuario = Column(String(10), nullable=False)
    direccion_usuario = Column(String(255), nullable=False)
    telefono_usuario = Column(String(20), nullable=False, unique=True)
    email_usuario = Column(String(100), nullable=False, unique=True)
    contrasena_usuario = Column (String(255), nullable=False, unique=True)
    
    fecha_registro = Column(DateTime, server_default=func.now())
    estatus_usuario = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    rol = relationship('Roles', back_populates='usuario')

    asignatura = relationship('Asignaturas', back_populates='usuario') # Usuario-Docente
    asistencia = relationship('Asistencias', back_populates='usuario') # Usuario-Estudiante
    inscripcion = relationship('Inscripciones', back_populates='usuario') # Usuario-Estudiante
    nota_final = relationship("Notas_Finales", back_populates="usuario") # Usuario-Estudiante