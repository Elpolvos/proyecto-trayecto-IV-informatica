from sqlalchemy.orm import Session
from datetime import date
from backend.src.models.models_asistencia import Asistencias
from backend.src.schemas.schemas_asistencia import AsistenciaCreate, AsistenciaEstatusUpdate, AsistenciaPresenteUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las asistencias

def get_asistencias(db: Session):

    logger.info(f"Todas las asistencias obtenidas exitosamente.")    

    return db.query(Asistencias).all()

# Obtener una asistencia por ID

def get_asistencia_por_id(db: Session, id_asistencia: int):
    
    logger.info(f"Asistencia ID: {Asistencias.id_asistencia} obtenida exitosamente")    
    
    return db.query(Asistencias).filter(Asistencias.id_asistencia == id_asistencia).first()

# Obtener todas las asistencias de un usuario-estudiante

def get_asistencias_por_estudiante(db: Session, fk_usuario_id: int):

    logger.info(f"Asistencias del estudiante: {Asistencias.fk_usuario_id} obtenidas exitosamente")

    return db.query(Asistencias).filter(Asistencias.fk_usuario_id == fk_usuario_id).all()

# Obtener todas las asistencias en una asignatura

def get_asistencias_por_asignatura(db: Session, fk_asignatura_id: int):
    
    logger.info(f"Asistencias en la asignatura: {Asistencias.fk_asignatura_id} obtenidas exitosamente")    

    return db.query(Asistencias).filter(Asistencias.fk_asignatura_id == fk_asignatura_id).all()

# Obtener todas las asistencias por fecha

def get_asistencias_por_fecha(db: Session, fecha: date):

    logger.info(f"Asistencias del día: {Asistencias.fecha_asistencia} obtenidas exitosamente")    

    return db.query(Asistencias).filter(Asistencias.fecha_asistencia == fecha).all()

# Obtener una asistencia por estudiante, que esté relacionada con una asignatura y a su vez con una fecha

def get_asistencia_por_estudiante_asignatura_fecha(db: Session, fk_usuario_id: int, fk_asignatura_id: int, fecha: date):
    
    logger.info(f"Asistencia del estudiante: {fk_usuario_id}, en la asignatura: {fk_asignatura_id}, del dia: {fecha} obtenida exitosamente")
    
    return db.query(Asistencias).filter(
        Asistencias.fk_usuario_id == fk_usuario_id,
        Asistencias.fk_asignatura_id == fk_asignatura_id,
        Asistencias.fecha_asistencia == fecha
    ).first()

# Crear una asistencia

def create_asistencia(db: Session, asistencia: AsistenciaCreate):

    logger.info(f"Creando nueva asistencia con fecha de asistencia: {asistencia.fecha_asistencia}")

    db_asistencia = Asistencias(fk_usuario_id=asistencia.fk_usuario_id,
                                fk_asignatura_id=asistencia.fk_asignatura_id,
                                fecha_asistencia=asistencia.fecha_asistencia,
                                presente=asistencia.presente
                                )
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)

    logger.info(f"Asistencia creada exitosamente - ID: {db_asistencia.id_asistencia}")    

    return db_asistencia

# Actualizar una asistencia por ID

def update_asistencia(db: Session, id_asistencia: int, asistencia: AsistenciaCreate):

    logger.info(f"Actualizando asistencia ID: {id_asistencia}")

    db_asistencia = db.query(Asistencias).filter(Asistencias.id_asistencia == id_asistencia).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_asistencia.__dict__, default=str)}")

    if db_asistencia:
        db_asistencia.fk_usuario_id = asistencia.fk_usuario_id
        db_asistencia.fk_asignatura_id = asistencia.fk_asignatura_id
        db_asistencia.fecha_asistencia = asistencia.fecha_asistencia
        db_asistencia.presente = asistencia.presente
        db.commit()
        db.refresh(db_asistencia)

    logger.info(f"Asistencia ID: {id_asistencia} actualizada exitosamente")

    return db_asistencia

# Actualizar el presente de una asistencia por ID

def update_presente_asistencia(db: Session, id_asistencia: int, asistencia: AsistenciaPresenteUpdate):

    logger.info(f"Actualizando el presente de la asistencia ID: {id_asistencia}")

    db_asistencia = db.query(Asistencias).filter(Asistencias.id_asistencia == id_asistencia).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_asistencia.__dict__, default=str)}")

    if db_asistencia:
        db_asistencia.presente = asistencia.presente
        db.commit()
        db.refresh(db_asistencia)

    logger.info(f"El estado del presente de la asistencia ID: {id_asistencia} se ha actualizado exitosamente")

    return db_asistencia

# Actualizar el estatus de una nota por ID (Soft-Delete)

def update_estatus_asistencia(db: Session, id_asistencia: int, asistencia: AsistenciaEstatusUpdate):

    logger.info(f"Actualizando el presente de la asistencia ID: {id_asistencia}")

    db_asistencia = db.query(Asistencias).filter(Asistencias.id_asistencia == id_asistencia).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_asistencia.__dict__, default=str)}")

    if db_asistencia:
        db_asistencia.estatus_asistencia = asistencia.estatus_asistencia
        db.commit()
        db.refresh(db_asistencia)

    logger.info(f"El estatus de la asistencia ID: {id_asistencia} se ha actualizado exitosamente")

    return db_asistencia

# Eliminar una nota por ID

def delete_asistencia(db: Session, id_asistencia: int):

    logger.warning(f"ELIMINANDO asistencia ID: {id_asistencia} - Esta acción es permanente")

    db_asistencia = db.query(Asistencias).filter(Asistencias.id_asistencia == id_asistencia).first()
    db.delete(db_asistencia)
    db.commit()

    logger.warning(f"Asistenc ID: {id_asistencia} eliminado permanentemente")

    return db_asistencia