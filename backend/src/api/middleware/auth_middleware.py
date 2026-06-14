from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.orm import Session
from backend.src.api.deps import get_db
from backend.src.models.models_administrador import Administradores
from backend.src.models.models_docente import Docentes
from backend.src.models.models_estudiante import Estudiantes

security = HTTPBearer()
SECRET_KEY = "pepetoño"  # Mismo que en auth.py
ALGORITHM = "HS256"

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Obtiene el usuario actual basado en el token JWT"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user_tipo = payload.get("tipo")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    if user_tipo == "admin":
        user = db.query(Administradores).filter(Administradores.id_administrador == user_id).first()
        if not user or not user.estatus_administrador:
            raise HTTPException(status_code=401, detail="Usuario no válido")
        user.tipo = "admin"
        return user
    
    elif user_tipo == "docente":
        user = db.query(Docentes).filter(Docentes.id_docente == user_id).first()
        if not user or not user.estatus_docente:
            raise HTTPException(status_code=401, detail="Usuario no válido")
        user.tipo = "docente"
        return user
    
    elif user_tipo == "estudiante":
        user = db.query(Estudiantes).filter(Estudiantes.id_estudiante == user_id).first()
        if not user or not user.estatus_estudiante:
            raise HTTPException(status_code=401, detail="Usuario no válido")
        user.tipo = "estudiante"
        return user
    
    raise HTTPException(status_code=401, detail="Tipo de usuario no válido")

def require_admin(current_user = Depends(get_current_user)):
    """Verifica que el usuario sea administrador"""
    if current_user.tipo != "admin":
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")
    return current_user

def require_docente(current_user = Depends(get_current_user)):
    """Verifica que el usuario sea docente o admin"""
    if current_user.tipo not in ["admin", "docente"]:
        raise HTTPException(status_code=403, detail="Se requieren permisos de docente")
    return current_user