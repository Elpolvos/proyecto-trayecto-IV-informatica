from sqlalchemy import Column, Integer, String, Date, Boolean
from backend.src.db.base_class import Base

class Administradores(Base):
    id_administrador = Column(Integer, primary_key=True, index=True)
    dni_administrador = Column(String(20), unique=True, nullable=False, index=True)
    apellido_administrador = Column(String(100), nullable=False)
    nombre_administrador = Column(String(100), nullable=False)
    fechanacimiento_administrador = Column(Date)
    sexo_administrador = Column(String(10), nullable=False)
    direccion_administrador = Column(String(255), nullable=False)
    telefono_administrador = Column(String(20), nullable=False, unique=True)
    email_administrador = Column(String(100), nullable=False, unique=True)
    contrasena_administrador = Column (String(255), nullable=False, unique=True)
    estatus_administrador = Column(Boolean, default=True, server_default="true")