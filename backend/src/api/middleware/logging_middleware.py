# src/middleware/logging_middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import json
from backend.src.core.logging import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Registrar inicio de request
        start_time = time.time()
        
        # Obtener información de la request
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)
        
        # Log de request entrante
        logger.info(f"REQUEST | {method} {url} | IP: {client_ip}")
        
        # Procesar request
        try:
            response = await call_next(request)
            
            # Calcular tiempo de respuesta
            process_time = time.time() - start_time
            
            # Log de respuesta
            logger.info(
                f"RESPONSE | {method} {url} | "
                f"Status: {response.status_code} | "
                f"Tiempo: {process_time:.3f}s"
            )
            
            # Agregar header con tiempo de respuesta
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            logger.error(f"ERROR | {method} {url} | {str(e)}", exc_info=True)
            raise