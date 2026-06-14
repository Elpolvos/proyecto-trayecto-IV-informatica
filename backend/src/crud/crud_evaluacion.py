from sqlalchemy.orm import Session
from backend.src.models.models_evaluacion import Evaluaciones
from backend.src.schemas.schemas_evaluacion import EvaluacionCreate, EvaluacionEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las evaluaciones

def get_evaluaciones(db: Session):

    logger.info(f"Todas las evaluaciones obtenidas exitosamente.")    

    return db.query(Evaluaciones).all()

# Obtener una las evaluaciones por ID

def get_evaluacion_por_id(db: Session, id_evaluacion: int):

    logger.info(f"Evaluacion ID: {Evaluaciones.id_evaluacion} obtenida exitosamente")

    return db.query(Evaluaciones).filter(Evaluaciones.id_evaluacion == id_evaluacion).first()

# Obtener todas las evaluaciones pertenecientes a una asignatura

def get_evaluaciones_por_asignatura(db: Session, fk_asignatura_id: int):

    logger.info(f"Evaluaciones de la asignatura: {Evaluaciones.fk_asignatura_id} obtenidas exitosamente")

    return db.query(Evaluaciones).filter(Evaluaciones.fk_asignatura_id == fk_asignatura_id).all()

# Obtener todas las evaluaciones del trimestre

def get_evaluaciones_por_trimestre(db: Session, fk_trimestre_id: int):

    logger.info(f"Evaluaciones del trimestre: {Evaluaciones.fk_trimestre_id} obtenidas exitosamente")

    return db.query(Evaluaciones).filter(Evaluaciones.fk_trimestre_id == fk_trimestre_id).all()

# Crear una evaluacion

def create_evaluacion(db: Session, evaluacion: EvaluacionCreate):

    logger.info(f"Creando nueva evaluacion con descripcion: {evaluacion.descripcion_evaluacion}")

    db_evaluacion = Evaluaciones(fk_asignatura_id = evaluacion.fk_asignatura_id,
                                 fk_trimestre_id = evaluacion.fk_trimestre_id,
                                 numero_evaluacion = evaluacion.numero_evaluacion,
                                 descripcion_evaluacion = evaluacion.descripcion_evaluacion,
                                 porcentaje_evaluacion = evaluacion.porcentaje_evaluacion,
                                 puntuacion_nota = evaluacion.puntuacion_nota,
                                 acumulativo = evaluacion.acumulativo,
                                 fecha_registro = evaluacion.fecha_registro
                                 )
    db.add(db_evaluacion)
    db.commit()
    db.refresh(db_evaluacion)

    logger.info(f"Evaluacion creada exitosamente - ID: {db_evaluacion.id_evaluacion}")    

    return db_evaluacion

# Actualizar una evaluacion por ID

def update_evaluacion(db: Session, id_evaluacion: int, evaluacion: EvaluacionCreate):

    logger.info(f"Actualizando evaluacion ID: {id_evaluacion}")

    db_evaluacion = db.query(Evaluaciones).filter(Evaluaciones.id_evaluacion == id_evaluacion).first()

    if db_evaluacion:    
        db_evaluacion.fk_asignatura_id = evaluacion.fk_asignatura_id
        db_evaluacion.fk_trimestre_id = evaluacion.fk_trimestre_id
        db_evaluacion.numero_evaluacion = evaluacion.numero_evaluacion
        db_evaluacion.descripcion_evaluacion = evaluacion.descripcion_evaluacion
        db_evaluacion.porcentaje_evaluacion = evaluacion.porcentaje_evaluacion
        db_evaluacion.puntuacion_nota = evaluacion.puntuacion_nota
        db_evaluacion.acumulativo = evaluacion.acumulativo
        db_evaluacion.fecha_registro = evaluacion.fecha_registro
        db.commit()
        db.refresh(db_evaluacion)

    logger.info(f"Evaluacion ID: {id_evaluacion} actualizada exitosamente")

    return db_evaluacion

# Actualizar el estatus de una evaluacion por ID (Soft-Delete)

def update_estatus_evaluacion(db: Session, id_evaluacion: int, evaluacion: EvaluacionEstatusUpdate):
    
    logger.info(f"Actualizando el estatus de la evaluacion ID: {id_evaluacion}")
    
    db_evaluacion = db.query(Evaluaciones).filter(Evaluaciones.id_evaluacion == id_evaluacion).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_evaluacion.__dict__, default=str)}")

    if db_evaluacion:    
        db_evaluacion.estatus_evaluacion = evaluacion.estatus_evaluacion
        db.commit()
        db.refresh(db_evaluacion)

    logger.info(f"El estatus de la evaluacion ID: {id_evaluacion} ha sido actualizado exitosamente")

    return db_evaluacion

# Eliminar una evaluacion por ID

def delete_evaluacion(db: Session, id_evaluacion: int):
    
    logger.warning(f"ELIMINANDO evaluacion ID: {id_evaluacion} - Esta acción es permanente")
    
    db_evaluacion = db.query(Evaluaciones).filter(Evaluaciones.id_evaluacion == id_evaluacion).first()
    db.delete(db_evaluacion)
    db.commit()

    logger.warning(f"Evaluacion ID: {id_evaluacion} eliminada permanentemente")

    return db_evaluacion