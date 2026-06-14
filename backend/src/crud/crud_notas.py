from sqlalchemy.orm import Session
from backend.src.models.models_notas import Notas
from backend.src.schemas.schemas_notas import NotaCreate, NotaEstatusUpdate, NotaPuntuacionUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las notas

def get_notas(db: Session):

    logger.info(f"Todas las notas obtenidas exitosamente.")    

    return db.query(Notas).all()

# Obtener una nota por ID

def get_nota_por_id(db: Session, id_nota: int):

    logger.info(f"Nota ID: {Notas.id_nota} obtenida exitosamente")

    return db.query(Notas).filter(Notas.id_nota == id_nota).first()

# Obtener todas las notas por estudiante 

def get_notas_por_estudiante(db: Session, id_estudiante: int):

    logger.info(f"Notas del estudiante: {Notas.fk_estudiante_id} obtenidas exitosamente")

    return db.query(Notas).filter(Notas.fk_estudiante_id == id_estudiante).all()

# Obtener todas las notas por evaluacion

def get_notas_por_evaluacion(db: Session, id_evaluacion: int):

    logger.info(f"Notas referentes a la evaluacion: {Notas.fk_evaluacion_id} obtenidas exitosamente")

    return db.query(Notas).filter(Notas.fk_evaluacion_id == id_evaluacion).all()

# Obtener una nota por estudiante que esté relacionada con una evaluacion.

def get_nota_por_estudiante_evaluacion(db: Session, id_estudiante: int, id_evaluacion: int):

    logger.info(f"Nota del estudiante: {Notas.fk_estudiante_id} referente a la evaluacion: {Notas.fk_evaluacion_id} obtenida exitosamente")

    return db.query(Notas).filter(
        Notas.fk_estudiante_id == id_estudiante,
        Notas.fk_evaluacion_id == id_evaluacion
    ).first()

# Crear una nota

def create_nota(db: Session, nota: NotaCreate):

    logger.info(f"Creando nueva nota con puntuacion: {nota.puntuacion_nota}")

    db_nota = Notas(id_evaluacion = nota.id_evaluacion,
                    id_estudiante = nota.id_estudiante,
                    puntuacion_nota = nota.puntuacion_nota
                    )
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)

    logger.info(f"Nota creada exitosamente - ID: {db_nota.id_nota}")    

    return db_nota

# Actualizar una nota por ID

def update_nota(db: Session, id_nota: int, nota: NotaCreate):

    logger.info(f"Actualizando nota ID: {id_nota}")

    db_nota = db.query(Notas).filter(Notas.id_nota == id_nota).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_nota.__dict__, default=str)}")

    if db_nota:
        db_nota.fk_evaluacion_id = nota.id_evaluacion
        db_nota.fk_estudiante_id = nota.id_estudiante
        db_nota.puntuacion_nota = nota.puntuacion_nota
        db.commit()
        db.refresh(db_nota)

    logger.info(f"Nota ID: {id_nota} actualizada exitosamente")

    return db_nota

# Actualizar la puntuacion de una nota por ID

def update_puntuacion_nota(db: Session, id_nota: int, nota: NotaPuntuacionUpdate):

    logger.info(f"Actualizando la puntuacion de la nota ID: {id_nota}")

    db_nota = db.query(Notas).filter(Notas.id_nota == id_nota).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_nota.__dict__, default=str)}")

    if db_nota:
        db_nota.puntuacion_nota = nota.puntuacion_nota
        db.commit()
        db.refresh(db_nota)

    logger.info(f"La puntuacion de la nota ID: {id_nota} ha sido actualizada exitosamente")

    return db_nota

# Actualizar el estatus de una nota por ID (Soft-Delete)

def update_estatus_nota(db: Session, id_nota: int, nota: NotaEstatusUpdate):

    logger.info(f"Actualizando el estatus de la nota ID: {id_nota}")

    db_nota = db.query(Notas).filter(Notas.id_nota == id_nota).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_nota.__dict__, default=str)}")

    if db_nota:
        db_nota.estatus_nota = nota.estatus_nota
        db.commit()
        db.refresh(db_nota)

    logger.info(f"El estatus de la nota ID: {id_nota} ha sido actualizado exitosamente")

    return db_nota

# Eliminar una nota por ID

def delete_nota(db: Session, id_nota: int):

    logger.warning(f"ELIMINANDO nota ID: {id_nota} - Esta acción es permanente")

    db_nota = db.query(Notas).filter(Notas.id_nota == id_nota).first()
    db.delete(db_nota)
    db.commit()

    logger.warning(f"Nota ID: {id_nota} eliminada permanentemente")

    return db_nota