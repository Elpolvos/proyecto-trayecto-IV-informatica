from sqlalchemy.orm import Session
from backend.src.models.models_inscripcion import Inscripciones
from backend.src.schemas.schemas_inscripcion import InscripcionCreate, InscripcionEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las inscripciones

def get_inscripciones(db: Session):

    logger.info(f"Todas las inscripciones obtenidas exitosamente.")    

    return db.query(Inscripciones).all()

# Obtener una inscripcion por ID

def get_inscripcion_por_id(db: Session, id_inscripcion: int):

    logger.info(f"Inscripcion ID: {Inscripciones.id_inscripcion} obtenido exitosamente")

    return db.query(Inscripciones).filter(Inscripciones.id_inscripcion == id_inscripcion).first()

# Obtener una inscripcion por usuario-estudiante

def get_inscripciones_por_estudiante(db: Session, fk_usuario_id: int):

    logger.info(f"Inscripcion perteneciente al estudiante: {Inscripciones.fk_usuario_id} obtenido exitosamente")

    return db.query(Inscripciones).filter(Inscripciones.fk_usuario_id == fk_usuario_id).first()

# Obtener todas las inscripciones referentes a una seccion

def get_inscripciones_por_seccion(db: Session, fk_seccion_id: int):
    
    logger.info(f"Inscripciones referentes al {Inscripciones.fk_seccion_id} obtenidas exitosamente")
    
    return db.query(Inscripciones).filter(Inscripciones.fk_seccion_id == fk_seccion_id).all()

# Obtener todas las inscripciones del año escolar

def get_inscripciones_por_anio_escolar(db: Session, anio_escolar: int):

    logger.info(f"Inscripciones referentes al anio escolar: {Inscripciones.anio_escolar} obtenidas exitosamente")

    return db.query(Inscripciones).filter(Inscripciones.anio_escolar == anio_escolar).all()

# Obtener una inscripcion por estudiante que esté relacionado a un año escolar

def get_inscripcion_por_estudiante_anio(db: Session, fk_usuario_id: int, anio_escolar: int):

    logger.info(f"Inscripcion del estudiante: {fk_usuario_id} en el anio escolar: {anio_escolar} obtenido exitosamente")

    return db.query(Inscripciones).filter(
        Inscripciones.fk_usuario_id == fk_usuario_id,
        Inscripciones.anio_escolar == anio_escolar
    ).first()

# Crear una inscripcion

def create_inscripcion(db: Session, inscripcion: InscripcionCreate):

    logger.info(f"Creando nueva inscripcion con fecha: {inscripcion.fecha_inscripcion}")

    db_inscripcion = Inscripciones(fk_usuario_id=inscripcion.fk_usuario_id,
                                   fk_seccion_id=inscripcion.fk_seccion_id,
                                   fecha_inscripcion=inscripcion.fecha_inscripcion,
                                   anio_escolar=inscripcion.anio_escolar
                                   )
    db.add(db_inscripcion)
    db.commit()
    db.refresh(db_inscripcion)

    logger.info(f"Inscripcion creada exitosamente - ID: {db_inscripcion.id_inscripcion}")    

    return db_inscripcion

# Actualizar una inscripcion por ID

def update_inscripcion(db: Session, id_inscripcion: int, inscripcion: InscripcionCreate):

    logger.info(f"Actualizando inscripcion ID: {id_inscripcion}")

    db_inscripcion = db.query(Inscripciones).filter(Inscripciones.id_inscripcion == id_inscripcion).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_inscripcion.__dict__, default=str)}")

    if db_inscripcion:
        db_inscripcion.fk_usuario_id = inscripcion.fk_usuario_id
        db_inscripcion.fk_seccion_id = inscripcion.fk_seccion_id
        db_inscripcion.fecha_inscripcion = inscripcion.fecha_inscripcion
        db_inscripcion.anio_escolar = inscripcion.anio_escolar
        db.commit()
        db.refresh(db_inscripcion)

    logger.info(f"Inscripcion ID: {id_inscripcion} actualizada exitosamente")

    return db_inscripcion

# Actualizar el estatus de una nota por ID (Soft-Delete)

def update_status_inscripcion(db: Session, id_inscripcion: int, inscripcion: InscripcionEstatusUpdate):

    logger.info(f"Actualizando el estatus de la inscripcion ID: {id_inscripcion}")

    db_inscripcion = db.query(Inscripciones).filter(Inscripciones.id_inscripcion == id_inscripcion).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_inscripcion.__dict__, default=str)}")

    if db_inscripcion:
        db_inscripcion.estatus_inscripcion = inscripcion.estatus_inscripcion
        db.commit()
        db.refresh(db_inscripcion)

    logger.info(f"El estatus de la inscripcion ID: {id_inscripcion} ha sido actualizado exitosamente")

    return db_inscripcion

# Eliminar una nota por ID

def delete_inscripcion(db: Session, id_inscripcion: int):

    logger.warning(f"ELIMINANDO inscripcion ID: {id_inscripcion} - Esta acción es permanente")

    db_inscripcion = db.query(Inscripciones).filter(Inscripciones.id_inscripcion == id_inscripcion).first()
    db.delete(db_inscripcion)
    db.commit()

    logger.warning(f"Inscripcion ID: {id_inscripcion} eliminada permanentemente")

    return db_inscripcion