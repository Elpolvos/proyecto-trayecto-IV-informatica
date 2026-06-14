from sqlalchemy.orm import Session
from backend.src.models.models_asignatura import Asignaturas
from backend.src.schemas.schemas_asignatura import AsignaturaCreate, AsignaturaEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las asignaturas

def get_asignaturas(db: Session):

    logger.info(f"Todas las asignaturas obtenidas exitosamente.")    

    return db.query(Asignaturas).all()

# Obtener una asignaturas por ID

def get_asignatura_por_id(db: Session, id_asignatura: int):
    
    logger.info(f"Asignatura ID: {Asignaturas.id_asignatura} obtenida exitosamente")
    
    return db.query(Asignaturas).filter(Asignaturas.id_asignatura == id_asignatura).first()

# Obtener todas las asignaturas por usuario-docente

def get_asignaturas_por_docente(db: Session, fk_ususario_id: int):

    logger.info(f"Asignaturas que enseña el docente: {Asignaturas.fk_usuario_id} obtenidas exitosamente")

    return db.query(Asignaturas).filter(Asignaturas.fk_usuario_id == fk_ususario_id).all()

# Obtener todas las asignaturas por seccion

def get_asignaturas_por_seccion(db: Session, fk_seccion_id: int):

    logger.info(f"Asignaturas que se ven en: {Asignaturas.fk_seccion_id} obtenidas exitosamente")

    return db.query(Asignaturas).filter(Asignaturas.fk_seccion_id == fk_seccion_id).all()

# Crear una asignatura o materia.

def create_asignatura(db: Session, asignatura: AsignaturaCreate):

    logger.info(f"Creando nueva asignatura con nombre: {asignatura.nombre_asignatura}")

    db_asignatura = Asignaturas(fk_ususario_id = asignatura.fk_usuario_id,
                                fk_seccion_id = asignatura.fk_seccion_id,
                                nombre_asignatura = asignatura.nombre_asignatura,
                                contenido_asignatura = asignatura.contenido_asignatura,
                                hora_inicio = asignatura.hora_inicio,
                                hora_fin = asignatura.hora_fin
                                )
    db.add(db_asignatura)
    db.commit()
    db.refresh(db_asignatura)

    logger.info(f"Asignatura creada exitosamente - ID: {db_asignatura.id_asignatura}")    

    return db_asignatura

# Actualizar una asignatura por ID

def update_asignatura(db: Session, id_asignatura: int, asignatura: AsignaturaCreate):

    logger.info(f"Actualizando asignatura ID: {id_asignatura}")

    db_asignatura = db.query(Asignaturas).filter(Asignaturas.id_asignatura == id_asignatura).first()
    
    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_asignatura.__dict__, default=str)}")

    if db_asignatura:
        db_asignatura.fk_usuario_id = asignatura.fk_usuario_id
        db_asignatura.fk_seccion_id = asignatura.fk_seccion_id
        db_asignatura.nombre_asignatura = asignatura.nombre_asignatura
        db_asignatura.contenido_asignatura = asignatura.contenido_asignatura
        db_asignatura.hora_inicio = asignatura.hora_inicio
        db_asignatura.hora_fin = asignatura.hora_fin
        db.commit()
        db.refresh(db_asignatura)

    logger.info(f"Asignatura ID: {id_asignatura} actualizada exitosamente")

    return db_asignatura

# Actualizar el estatus de una asignatura por ID (Soft-Delete)

def update_estatus_asignatura(db: Session, id_asignatura: int, asignatura: AsignaturaEstatusUpdate):

    logger.info(f"Actualizando el estatus de la asignatura ID: {id_asignatura}")

    db_asignatura = db.query(Asignaturas).filter(Asignaturas.id_asignatura == id_asignatura).first()
    
    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_asignatura.__dict__, default=str)}")
    
    if db_asignatura:
        db_asignatura.estatus_asignatura = asignatura.estatus_asignatura
        db.commit()
        db.refresh(db_asignatura)

    logger.info(f"El estatus de la asignatura ID: {id_asignatura} ha sido actualizado exitosamente")

    return db_asignatura

# Eliminar una asignatura por ID

def delete_asignatura(db: Session, id_asignatura: int):

    logger.warning(f"ELIMINANDO asignatura ID: {id_asignatura} - Esta acción es permanente")

    db_asignatura = db.query(Asignaturas).filter(Asignaturas.id_asignatura == id_asignatura).first()
    db.delete(db_asignatura)
    db.commit()

    logger.warning(f"Asignatura ID: {id_asignatura} eliminada permanentemente")

    return db_asignatura