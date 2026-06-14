from sqlalchemy.orm import Session
from backend.src.models.models_seccion import Secciones
from backend.src.schemas.schemas_seccion import SeccionCreate, SeccionEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las secciones

def get_secciones(db: Session):

    logger.info(f"Todas las secciones obtenidas exitosamente.")    

    return db.query(Secciones).all()

# Obtener una seccion por ID

def get_seccion_por_id(db: Session, id_seccion: int):

    logger.info(f"Seccion ID: {Secciones.id_seccion} obtenida exitosamente")

    return db.query(Secciones).filter(Secciones.id_seccion == id_seccion).first()

# Obtener una seccion por descripcion

def get_seccion_por_descripcion(db: Session, descripcion: str):

    logger.info(f"Seccion cuya descripcion es: {Secciones.descripcion_seccion} ha sido obtenida exitosamente")

    return db.query(Secciones).filter(Secciones.descripcion_seccion == descripcion).first()

# Crear una seccion

def create_seccion(db: Session, seccion: SeccionCreate):

    logger.info(f"Creando nueva seccion con descripcion: {seccion.descripcion_seccion}")

    db_seccion = Secciones(descripcion_seccion = seccion.descripcion_seccion)
    db.add(db_seccion)
    db.commit()
    db.refresh(db_seccion)

    logger.info(f"Seccion creada exitosamente - ID: {db_seccion.id_seccion}")    

    return db_seccion

# Actualizar una seccion por ID

def update_seccion(db: Session, id_seccion: int, seccion: SeccionCreate):

    logger.info(f"Actualizando seccion ID: {id_seccion}")

    db_seccion = db.query(Secciones).filter(Secciones.id_seccion == id_seccion).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_seccion.__dict__, default=str)}")

    if db_seccion:
        db_seccion.descripcion_seccion = seccion.descripcion_seccion
        db.commit()
        db.refresh(db_seccion)

    logger.info(f"Seccion ID: {id_seccion} actualizada exitosamente")

    return db_seccion

# Actualizar el estatus de una seccion por ID (Soft-Delete)

def update_estatus_seccion(db: Session, id_seccion: int, seccion: SeccionEstatusUpdate):

    logger.info(f"Actualizando el estatus de la seccion ID: {id_seccion}")

    db_seccion = db.query(Secciones).filter(Secciones.id_seccion == id_seccion).first()
    
    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_seccion.__dict__, default=str)}")

    if db_seccion:
        db_seccion.estatus_seccion = seccion.estatus_seccion
        db.commit()
        db.refresh(db_seccion)

    logger.info(f"El estatus de la seccion ID: {id_seccion} ha sido actualizado exitosamente")

    return db_seccion

# Eliminar una seccion por ID

def delete_seccion(db: Session, id_seccion: int):

    logger.warning(f"ELIMINANDO seccion ID: {id_seccion} - Esta acción es permanente")

    db_seccion = db.query(Secciones).filter(Secciones.id_seccion == id_seccion).first()
    db.delete(db_seccion)
    db.commit()

    logger.warning(f"Seccion ID: {id_seccion} eliminada permanentemente")

    return db_seccion