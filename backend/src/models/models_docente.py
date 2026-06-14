from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base

class Docentes(Base):
    id_docente = Column(Integer, primary_key=True, index=True)
    dni_docente = Column(String(20), unique=True, nullable=False, index=True)
    apellido_docente = Column(String(100), nullable=False)
    nombre_docente = Column(String(100), nullable=False)
    fechanacimiento_docente = Column(Date)
    sexo_docente = Column(String(10), nullable=False)
    direccion_docente = Column(String(255), nullable=False)
    telefono_docente = Column(String(20), unique=True, nullable=False)
    email_docente = Column(String(100), nullable=False, unique=True)
    contrasena_docente = Column (String(255), nullable=False, unique=True)
    estatus_docente = Column(Boolean, default=True, server_default="true")

    #RELACIONES

    #asignatura = relationship('Asignaturas', back_populates='docente')