import logging
import sys
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
import json
from sqlalchemy.orm import Session

# Crear directorio de logs si no existe
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configuración del logger principal
def setup_logging():
    """Configura el sistema de logging completo"""
    
    # Formato para archivos (detallado)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Formato para consola (más legible)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Logger principal de la aplicación
    app_logger = logging.getLogger("colegio_api")
    app_logger.setLevel(logging.DEBUG)
    
    # Handler para archivo - todos los logs
    file_handler = RotatingFileHandler(
        LOG_DIR / "colegio_api.log",
        maxBytes=10_485_760,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    app_logger.addHandler(file_handler)
    
    # Handler para archivo de errores específicamente
    error_handler = RotatingFileHandler(
        LOG_DIR / "errors.log",
        maxBytes=5_242_880,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    app_logger.addHandler(error_handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    app_logger.addHandler(console_handler)
    
    return app_logger

# Logger de auditoría (operaciones importantes)
audit_logger = logging.getLogger("auditoria")
audit_logger.setLevel(logging.INFO)

# Handler específico para auditoría
audit_handler = RotatingFileHandler(
    LOG_DIR / "auditoria.log",
    maxBytes=10_485_760,
    backupCount=20,
    encoding='utf-8'
)

audit_formatter = logging.Formatter(
    '%(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
audit_handler.setFormatter(audit_formatter)
audit_logger.addHandler(audit_handler)

# Obtener logger principal
logger = setup_logging()