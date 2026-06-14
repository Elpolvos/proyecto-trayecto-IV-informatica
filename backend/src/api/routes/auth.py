# backend/src/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy.orm import Session
from backend.src.api.deps import get_db
from backend.src.models.models_usuario import Usuarios
from backend.src.models.models_rol import Roles  # Asumiendo que tienes este modelo
from backend.src.crud import crud_usuario as usuario_crud
from backend.src.core.logging import logger
from backend.src.core.security import SecurityConfig

router = APIRouter(prefix="/api/v1/auth", tags=["autenticación"])

SECRET_KEY = SecurityConfig.SECRET_KEY
ALGORITHM = SecurityConfig.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES

# Esquemas Pydantic
class LoginRequest(BaseModel):
    email: str  # Puede ser email o DNI
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

class TokenData(BaseModel):
    id_usuario: int
    rol: str
    email: str

# Configuración de seguridad
security = HTTPBearer()

# Funciones auxiliares
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica la contraseña, soporta bcrypt y texto plano (solo desarrollo)
    """
    try:
        # Si la contraseña está encriptada con bcrypt
        if hashed_password.startswith('$2b$'):
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        # Si está en texto plano (solo para desarrollo)
        else:
            return plain_password == hashed_password
    except Exception as e:
        logger.error(f"Error verificando contraseña: {e}")
        return plain_password == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_rol_nombre(db: Session, rol_id: int) -> str:
    """
    Obtiene el nombre del rol por su ID
    """
    rol = db.query(Roles).filter(Roles.id_rol == rol_id).first()
    return rol.tipo_rol if rol else "desconocido"

# Endpoints de autenticación
@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest, 
    db: Session = Depends(get_db)
):
    """
    Login unificado que busca en la tabla de usuarios por email o DNI
    """
    logger.info(f"Intento de login con: {login_data.email}")
    
    # Buscar usuario por email o DNI
    usuario = None
    
    # Primero intentar por email
    usuario = usuario_crud.get_usuario_por_email(db, email=login_data.email)
    
    # Si no se encuentra por email, intentar por DNI
    if not usuario:
        usuario = usuario_crud.get_usuario_por_dni(db, dni_usuario=login_data.email)
    
    # Verificar si el usuario existe
    if not usuario:
        logger.warning(f"Login fallido - Usuario no encontrado: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/DNI o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar si el usuario está activo
    if not usuario.estatus_usuario:
        logger.warning(f"Login fallido - Usuario inactivo: {usuario.email_usuario}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo. Contacte al administrador.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar contraseña
    if not verify_password(login_data.password, usuario.contrasena_usuario):
        logger.warning(f"Login fallido - Contraseña incorrecta para: {usuario.email_usuario}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/DNI o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener el nombre del rol
    rol_nombre = get_rol_nombre(db, usuario.fk_rol_id)
    
    # Crear datos del usuario para la respuesta
    user_data = {
        "id": usuario.id_usuario,
        "nombre": usuario.nombre_usuario,
        "apellido": usuario.apellido_usuario,
        "dni": usuario.dni_usuario,
        "email": usuario.email_usuario,
        "tipo": rol_nombre,  # 'admin', 'docente', 'estudiante'
        "rol_id": usuario.fk_rol_id,
        "estatus": usuario.estatus_usuario,
        "telefono": usuario.telefono_usuario,
        "direccion": usuario.direccion_usuario
    }
    
    # Crear token JWT
    token_data = {
        "sub": str(usuario.id_usuario),
        "email": usuario.email_usuario,
        "rol": rol_nombre,
        "rol_id": usuario.fk_rol_id
    }
    access_token = create_access_token(data=token_data)
    
    logger.info(f"Login exitoso - Usuario: {usuario.email_usuario}, Rol: {rol_nombre}")
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data
    )

@router.post("/logout")
async def logout():
    """
    Cierre de sesión (el cliente debe eliminar el token)
    """
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/verify")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Verifica si un token es válido
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))
        
        # Verificar que el usuario aún existe y está activo
        usuario = usuario_crud.get_usuario_por_id(db, id_usuario=usuario_id)
        
        if not usuario or not usuario.estatus_usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o usuario inactivo"
            )
        
        return {
            "valid": True,
            "user_id": usuario_id,
            "email": usuario.email_usuario,
            "rol": payload.get("rol")
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

# Middleware/Dependencia para obtener usuario actual
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuarios:
    """
    Obtiene el usuario actual a partir del token JWT
    Esta función se puede usar como dependencia en otros endpoints
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub"))
        
        if usuario_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    usuario = usuario_crud.get_usuario_por_id(db, id_usuario=usuario_id)
    
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    if not usuario.estatus_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return usuario

def get_current_active_user(
    current_user: Usuarios = Depends(get_current_user),
) -> Usuarios:
    """
    Verifica que el usuario esté activo
    """
    if not current_user.estatus_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

# Dependencias para verificar roles específicos
def require_admin(
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Usuarios:
    """
    Verifica que el usuario sea administrador
    """
    rol_nombre = get_rol_nombre(db, current_user.fk_rol_id)
    
    if rol_nombre != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user

def require_docente(
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Usuarios:
    """
    Verifica que el usuario sea docente o administrador
    """
    rol_nombre = get_rol_nombre(db, current_user.fk_rol_id)
    
    if rol_nombre not in ["admin", "docente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de docente"
        )
    return current_user

def require_estudiante(
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Usuarios:
    """
    Verifica que el usuario sea estudiante
    """
    rol_nombre = get_rol_nombre(db, current_user.fk_rol_id)
    
    if rol_nombre != "estudiante":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para estudiantes"
        )
    return current_user