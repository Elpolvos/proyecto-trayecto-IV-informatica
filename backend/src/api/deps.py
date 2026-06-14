from typing import Generator
from backend.src.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Obtener usuario actual del token JWT"""
    token = credentials.credentials
    # Aquí decodificarías tu JWT
    # Por ahora, retornamos un usuario mock
    return {"username": "admin", "role": "admin"}