from sqlalchemy.orm import Session
from backend.src.models.models_aprobacion import Estados_Aprobaciones
from backend.src.schemas.schemas_aprobacion import AprobacionCreate, AprobacionEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los estados de aprobacion

def get_aprobaciones(db: Session):

    logger.info(f"Todos los estados de aprobacion obtenidos exitosamente.")    

    return db.query(Estados_Aprobaciones).all()

# Obtener un estado de aprobacion por ID

def get_aprobacion_por_id(db: Session, id_estado_aprobacion: int):

    logger.info(f"Estado de aprobacion ID: {Estados_Aprobaciones.id_estado_aprobacion} obtenido exitosamente")

    return db.query(Estados_Aprobaciones).filter(Estados_Aprobaciones.id_estado_aprobacion == id_estado_aprobacion).first()

# Obtener un estado de aprobacion por tipo

def get_aprobacion_por_tipo(db: Session, estado_aprobacion: str):

    logger.info(f"Estado de aprobacion cuyo tipo es: {Estados_Aprobaciones.estado_aprobacion} ha sido obtenido exitosamente")

    return db.query(Estados_Aprobaciones).filter(Estados_Aprobaciones.estado_aprobacion == estado_aprobacion).first()

# Crear un estado de aprobacion

def create_aprobacion(db: Session, aprobacion: AprobacionCreate):

    logger.info(f"Creando nuevo estado de aprobacion llamado: {aprobacion.estado_aprobacion}")

    db_estado_aprobacion = Estados_Aprobaciones(estado_aprobacion = aprobacion.estado_aprobacion)
    db.add(db_estado_aprobacion)
    db.commit()
    db.refresh(db_estado_aprobacion)

    logger.info(f"Estado de aprobacion creado exitosamente - ID: {db_estado_aprobacion.id_estado_aprobacion}")    

    return db_estado_aprobacion

# Actualizar un estado de aprobacion por ID

def update_aprobacion(db: Session, id_estado_aprobacion: int, aprobacion: AprobacionCreate):

    logger.info(f"Actualizando estado de aprobacion ID: {id_estado_aprobacion}")

    db_estado_aprobacion = db.query(Estados_Aprobaciones).filter(Estados_Aprobaciones.id_estado_aprobacion == id_estado_aprobacion).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_estado_aprobacion.__dict__, default=str)}")

    if db_estado_aprobacion:
        db_estado_aprobacion.estado_aprobacion = aprobacion.estado_aprobacion
        db.commit()
        db.refresh(db_estado_aprobacion)

    logger.info(f"Estado de aprobacion ID: {id_estado_aprobacion} actualizado exitosamente")

    return db_estado_aprobacion

# Actualizar el estatus de un estado de aprobacion por ID (Soft-Delete)

def update_estatus_aprobacion(db: Session, id_estado_aprobacion: int, aprobacion: AprobacionEstatusUpdate):

    logger.info(f"Actualizando el estatus del tipo de aprobacion ID: {id_estado_aprobacion}")

    db_estado_aprobacion = db.query(Estados_Aprobaciones).filter(Estados_Aprobaciones.id_estado_aprobacion == id_estado_aprobacion).first()
    
    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_estado_aprobacion.__dict__, default=str)}")

    if db_estado_aprobacion:
        db_estado_aprobacion.estatus_aprobacion = aprobacion.estatus_aprobacion
        db.commit()
        db.refresh(db_estado_aprobacion)

    logger.info(f"El estatus del tipo de aprobacion ID: {id_estado_aprobacion} ha sido actualizado exitosamente")

    return db_estado_aprobacion

# Eliminar un estado de aprobacion por ID

def delete_aprobacion(db: Session, id_estado_aprobacion: int):

    logger.warning(f"ELIMINANDO estado de aprobacion ID: {id_estado_aprobacion} - Esta acción es permanente")

    db_estado_aprobacion = db.query(Estados_Aprobaciones).filter(Estados_Aprobaciones.id_estado_aprobacion == id_estado_aprobacion).first()
    db.delete(db_estado_aprobacion)
    db.commit()

    logger.warning(f"Estado de aprobacion ID: {id_estado_aprobacion} eliminada permanentemente")

    return db_estado_aprobacion