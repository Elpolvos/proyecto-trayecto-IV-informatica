from sqlalchemy.orm import Session
from backend.src.models.models_rol import Roles
from backend.src.schemas.schemas_rol import RolCreate, RolEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los roles

def get_roles(db: Session):

    logger.info(f"Todos los roles obtenidas exitosamente.")    

    return db.query(Roles).all()

# Obtener un rol por ID

def get_rol_por_id(db: Session, id_rol: int):

    logger.info(f"Rol ID: {Roles.id_rol} obtenida exitosamente")

    return db.query(Roles).filter(Roles.id_rol == id_rol).first()

# Obtener un rol por tipo

def get_rol_por_tipo(db: Session, tipo_rol: str):

    logger.info(f"Rol cuyo tipo es: {Roles.tipo_rol} ha sido obtenida exitosamente")

    return db.query(Roles).filter(Roles.tipo_rol == tipo_rol).first()

# Crear un rol

def create_rol(db: Session, rol: RolCreate):

    logger.info(f"Creando nuevo rol llamado: {rol.tipo_rol}")

    db_rol = Roles(tipo_rol = rol.tipo_rol)
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)

    logger.info(f"Rol creada exitosamente - ID: {db_rol.id_rol}")    

    return db_rol

# Actualizar un rol por ID

def update_rol(db: Session, id_rol: int, rol: RolCreate):

    logger.info(f"Actualizando rol ID: {id_rol}")

    db_rol = db.query(Roles).filter(Roles.id_rol == id_rol).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_rol.__dict__, default=str)}")

    if db_rol:
        db_rol.tipo_rol = rol.tipo_rol
        db.commit()
        db.refresh(db_rol)

    logger.info(f"Rol ID: {id_rol} actualizada exitosamente")

    return db_rol

# Actualizar el estatus de un rol por ID (Soft-Delete)

def update_estatus_rol(db: Session, id_rol: int, rol: RolEstatusUpdate):

    logger.info(f"Actualizando el estatus del rol ID: {id_rol}")

    db_rol = db.query(Roles).filter(Roles.id_rol == id_rol).first()
    
    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_rol.__dict__, default=str)}")

    if db_rol:
        db_rol.estatus_rol = rol.estatus_rol
        db.commit()
        db.refresh(db_rol)

    logger.info(f"El estatus del rol ID: {id_rol} ha sido actualizado exitosamente")

    return db_rol

# Eliminar un rol por ID

def delete_rol(db: Session, id_rol: int):

    logger.warning(f"ELIMINANDO rol ID: {id_rol} - Esta acción es permanente")

    db_rol = db.query(Roles).filter(Roles.id_rol == id_rol).first()
    db.delete(db_rol)
    db.commit()

    logger.warning(f"Rol ID: {id_rol} eliminada permanentemente")

    return db_rol