# models_auditoria.py
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from backend.src.db.base_class import Base

class Auditoria(Base):
    
    id_log = Column(BigInteger, primary_key=True, index=True)
    usuario = Column(String(100), nullable=False)
    accion = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    tabla = Column(String(50))  # Nombre de la tabla afectada
    registro_id = Column(Integer)  # ID del registro afectado
    datos_anteriores = Column(Text)  # JSON con datos previos
    datos_nuevos = Column(Text)  # JSON con datos nuevos
    ip_origen = Column(String(45))  # IPv4 o IPv6
    user_agent = Column(String(255))
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())