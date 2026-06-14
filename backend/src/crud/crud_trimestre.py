from sqlalchemy.orm import Session
from backend.src.models.models_trimestre import Trimestres
from backend.src.schemas.schemas_trimestre import TrimestreCreate, TrimestreEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los trimestres

def get_trimestres(db: Session):

    logger.info(f"Todos los trimestres obtenidos exitosamente.")    

    return db.query(Trimestres).all()

# Obtener un trimestre por ID

def get_trimestre_por_id(db: Session, id_trimestre: int):

    logger.info(f"Trimestre ID: {Trimestres.id_trimestre} obtenido exitosamente")

    return db.query(Trimestres).filter(Trimestres.id_trimestre == id_trimestre).first()

# Obtener un trimestre por nombre

def get_trimestre_por_nombre(db: Session, nombre: str):

    logger.info(f"Trimestre de nombre: {Trimestres.nombre_trimestre} obtenido exitosamente")

    return db.query(Trimestres).filter(Trimestres.nombre_trimestre == nombre).first()

# Crear un trimestre

def create_trimestre(db: Session, trimestre: TrimestreCreate):

    logger.info(f"Creando nuevo trimestre con nombre: {trimestre.nombre_trimestre}")

    db_trimestre = Trimestres(nombre_trimestre=trimestre.nombre_trimestre,
                              fecha_inicio=trimestre.fecha_inicio,
                              fecha_fin=trimestre.fecha_fin
                              )
    db.add(db_trimestre)
    db.commit()
    db.refresh(db_trimestre)

    logger.info(f"Trimestre creado exitosamente - ID: {db_trimestre.id_trimestre}")    

    return db_trimestre

# Actualizar un trimestre por ID

def update_trimestre(db: Session, id_trimestre: int, trimestre: TrimestreCreate):

    logger.info(f"Actualizando trimestre ID: {id_trimestre}")

    db_trimestre = db.query(Trimestres).filter(Trimestres.id_trimestre == id_trimestre).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_trimestre.__dict__, default=str)}")

    if db_trimestre:
        db_trimestre.nombre_trimestre = trimestre.nombre_trimestre
        db_trimestre.fecha_inicio = trimestre.fecha_inicio
        db_trimestre.fecha_fin = trimestre.fecha_fin
        db.commit()
        db.refresh(db_trimestre)

    logger.info(f"Trimestre ID: {id_trimestre} actualizado exitosamente")

    return db_trimestre

# Actualizar el estatus de un trimestre por ID (Soft-Delete)

def update_estatus_trimestre(db: Session, id_trimestre: int, trimestre: TrimestreEstatusUpdate):

    logger.info(f"Actualizando el estatus del trimestre ID: {id_trimestre}")

    db_trimestre = db.query(Trimestres).filter(Trimestres.id_trimestre == id_trimestre).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_trimestre.__dict__, default=str)}")

    if db_trimestre:
        db_trimestre.estatus_trimestre = trimestre.estatus_trimestre
        db.commit()
        db.refresh(db_trimestre)

    logger.info(f"El estatus del trimestre ID: {id_trimestre} ha sido actualizado exitosamente")

    return db_trimestre

# Eliminar un trimestre por ID

def delete_trimestre(db: Session, id_trimestre: int):

    logger.warning(f"ELIMINANDO trimestre ID: {id_trimestre} - Esta acción es permanente")

    db_trimestre = db.query(Trimestres).filter(Trimestres.id_trimestre == id_trimestre).first()
    db.delete(db_trimestre)
    db.commit()

    logger.warning(f"Trimestre ID: {id_trimestre} eliminado permanentemente")

    return db_trimestre