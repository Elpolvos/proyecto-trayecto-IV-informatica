from sqlalchemy.orm import Session
from backend.src.models.models_administrador import Administradores
from backend.src.schemas.schemas_administrador import AdministradorCreate, AdministradorEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los administradores

def get_administradores(db: Session):
    
    logger.info(f"Todos los administradores obtenidos exitosamente")    

    return db.query(Administradores).all()

# Obtener un administrador por ID

def get_administrador_por_id(db: Session, id_admin: int):

    logger.info(f"Administrador ID: {Administradores.id_administrador} obtenido exitosamente")    

    return db.query(Administradores).filter(Administradores.id_administrador == id_admin).first()

# Obtener un administrador por DNI

def get_administrador_por_dni(db: Session, dni_admin: str):

    logger.info(f"Administrador DNI: {Administradores.dni_administrador} obtenido exitosamente")    

    return db.query(Administradores).filter(Administradores.dni_administrador == dni_admin).first()

# Crear un administrador

def create_administrador(db: Session, administrador: AdministradorCreate):
    
    logger.info(f"Creando nuevo administrador con DNI: {administrador.dni_administrador}")

    db_administrador = Administradores(dni_administrador = administrador.dni_administrador,
                                       apellido_administrador = administrador.apellido_administrador,
                                       nombre_administrador = administrador.nombre_administrador,
                                       fechanacimiento_administrador = administrador.fechanacimiento_administrador,
                                       sexo_administrador = administrador.sexo_administrador,
                                       direccion_administrador = administrador.direccion_administrador,
                                       telefono_administrador = administrador.telefono_administrador,
                                       email_administrador = administrador.email_administrador,
                                       contrasena_administrador = administrador.contrasena_administrador
                                       )
    db.add(db_administrador)
    db.commit()
    db.refresh(db_administrador)
    
    logger.info(f"Administrador creado exitosamente - ID: {db_administrador.id_administrador}")    

    return db_administrador

# Actualizar un administrador por ID

def update_administrador(db: Session, id_admin: int, admin: AdministradorCreate):
    
    logger.info(f"Actualizando administrador ID: {id_admin}")

    db_administrador = db.query(Administradores).filter(Administradores.id_administrador == id_admin).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_administrador.__dict__, default=str)}")

    if db_administrador:
        db_administrador.dni_administrador = admin.dni_administrador
        db_administrador.apellido_administrador = admin.apellido_administrador
        db_administrador.nombre_administrador = admin.nombre_administrador
        db_administrador.fechanacimiento_administrador = admin.fechanacimiento_administrador
        db_administrador.sexo_administrador = admin.sexo_administrador
        db_administrador.direccion_administrador = admin.direccion_administrador
        db_administrador.telefono_administrador = admin.telefono_administrador
        db_administrador.email_administrador = admin.email_administrador
        db_administrador.contrasena_administrador = admin.contrasena_administrador
        db.commit()
        db.refresh(db_administrador)
    
    logger.info(f"Administrador ID: {id_admin} actualizado exitosamente")

    return db_administrador

# Actualizar estatus de un administrador por ID (Soft-Delete)

def update_estatus_administrador(db: Session, id_admin: int, admin: AdministradorEstatusUpdate):

    logger.info(f"Actualizando el estatus del administrador ID: {id_admin}")

    db_administrador = db.query(Administradores).filter(Administradores.id_administrador == id_admin).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_administrador.__dict__, default=str)}")

    if db_administrador:
        db_administrador.estatus_administrador = admin.estatus_administrador
        db.commit()
        db.refresh(db_administrador)

    logger.info(f"El estatus del administrador ID: {id_admin} ha sido actualizado exitosamente")

    return db_administrador

# Eliminar un administrador por ID

def delete_administrador(db: Session, id_admin: int):
    
    logger.warning(f"ELIMINANDO administrador ID: {id_admin} - Esta acción es permanente")
    
    db_administrador = db.query(Administradores).filter(Administradores.id_administrador == id_admin).first()
    db.delete(db_administrador)
    db.commit()
    
    logger.warning(f"Administrador ID: {id_admin} eliminado permanentemente")
    
    return db_administrador