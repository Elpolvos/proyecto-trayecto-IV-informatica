# src/core/decorators.py
from functools import wraps
from sqlalchemy.orm import Session
from backend.src.core.logging import audit_logger
from backend.src.models.models_auditoria import Auditoria
from fastapi import Request
import json
import asyncio
from typing import Optional

def audit_action(accion: str, tabla: str):
    """Decorador para auditar acciones CRUD"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Buscar request en kwargs o args
            request = kwargs.get('request') or next(
                (arg for arg in args if isinstance(arg, Request)), None
            )
            
            # Buscar db session
            db = kwargs.get('db') or next(
                (arg for arg in args if isinstance(arg, Session)), None
            )
            
            # Obtener datos antes de la operación (si es UPDATE o DELETE)
            datos_anteriores = None
            if accion in ['UPDATE', 'DELETE']:
                id_registro = kwargs.get('id_administrador') or \
                             kwargs.get('id_estudiante') or \
                             kwargs.get('id_docente') or \
                             kwargs.get('id_asignatura')
                
                if id_registro and hasattr(func, '__model__'):
                    # Intentar obtener el registro actual
                    registro = db.query(func.__model__).filter(
                        getattr(func.__model__, f'id_{tabla.lower()}') == id_registro
                    ).first()
                    if registro:
                        datos_anteriores = json.dumps(registro.__dict__, default=str, indent=2)
            
            # Ejecutar la función original
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            # Registrar en auditoría
            usuario = "sistema"  # Aquí obtendrías el usuario del JWT
            
            audit_logger.info(
                f"USUARIO: {usuario} | ACCION: {accion} | "
                f"TABLA: {tabla} | ID: {kwargs.get('id_administrador') or 'N/A'} | "
                f"IP: {request.client.host if request else 'N/A'}"
            )
            
            # Guardar en BD si existe el modelo
            if db and request:
                log_db = Auditoria(
                    usuario=usuario,
                    accion=accion,
                    tabla=tabla,
                    registro_id=kwargs.get(f'id_{tabla.lower()}'),
                    datos_anteriores=datos_anteriores,
                    ip_origen=request.client.host if request.client else None,
                    user_agent=request.headers.get('user-agent')
                )
                db.add(log_db)
                db.commit()
            
            return result
        return wrapper
    return decorator