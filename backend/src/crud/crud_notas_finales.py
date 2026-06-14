from sqlalchemy.orm import Session
from backend.src.models.models_notas_finales import Notas_Finales
from backend.src.schemas.schemas_notas_finales import NotaFinalCreate, NotaFinalEstatusUpdate, NotaFinalPromedioUpdate

from backend.src.core.logging import logger
import json

# Obtener todas las notas finales

def get_notas_finales(db: Session):

    logger.info(f"Todas las notas finales obtenidas exitosamente.")    

    return db.query(Notas_Finales).all()

# Obtener una nota final por ID

def get_nota_final_por_id(db: Session, id_nota_final: int):

    logger.info(f"Nota final ID: {Notas_Finales.id_nota_final} obtenida exitosamente")

    return db.query(Notas_Finales).filter(Notas_Finales.id_nota_final == id_nota_final).first()

# Obtener todas las notas finales por usuario-estudiante

def get_notas_finales_por_estudiante(db: Session, fk_usuario_id: int):

    logger.info(f"Notas finales del estudiante: {Notas_Finales.fk_usuario_id} obtenidas exitosamente")

    return db.query(Notas_Finales).filter(Notas_Finales.fk_usuario_id == fk_usuario_id).all()

# Obtener todas las notas finales por asignatura

def get_notas_finales_por_asignatura(db: Session, fk_asignatura_id: int):

    logger.info(f"Notas finales en la asignatura: {Notas_Finales.fk_asignatura_id} obtenidas exitosamente")

    return db.query(Notas_Finales).filter(Notas_Finales.fk_asignatura_id == fk_asignatura_id).all()

# Obtener todas las notas finales por trimestre

def get_notas_finales_por_trimestre(db: Session, fk_trimestre_id: int):

    logger.info(f"Notas finales del trimestre: {Notas_Finales.fk_trimestre_id} obtenidas exitosamente")

    return db.query(Notas_Finales).filter(Notas_Finales.fk_trimestre_id == fk_trimestre_id).all()

# Obtener una nota final por estudiante que este relacionada con una asignatura y a su vez un trimestre

def get_nota_final_por_estudiante_asignatura_trimestre(db: Session, fk_usuario_id: int, fk_asignatura_id: int, fk_trimestre_id: int):

    logger.info(f"Notas finales del estudiante: {fk_usuario_id} en la asignatura: {fk_asignatura_id} durante el trimestre: {fk_trimestre_id} obtenidas exitosamente")

    return db.query(Notas_Finales).filter(
        Notas_Finales.fk_usuario_id == fk_usuario_id,
        Notas_Finales.fk_asignatura_id == fk_asignatura_id,
        Notas_Finales.fk_trimestre_id == fk_trimestre_id
    ).first()

# Crear una nota final

def create_nota_final(db: Session, nota_final: NotaFinalCreate):

    logger.info(f"Creando nueva nota final con estado de aprobacion: {nota_final.estado_aprobacion}")

    db_nota_final = Notas_Finales(fk_usuario_id = nota_final.fk_usuario_id,
                                  fk_asignatura_id=nota_final.fk_asignatura_id,
                                  fk_trimestre_id=nota_final.fk_trimestre_id,
                                  nota_promedio=nota_final.nota_promedio,
                                  porcentaje_asistencia=nota_final.porcentaje_asistencia,
                                  estado_aprobacion=nota_final.estado_aprobacion
                                  )
    db.add(db_nota_final)
    db.commit()
    db.refresh(db_nota_final)

    logger.info(f"Nota final creada exitosamente - ID: {db_nota_final.id_nota_final}")    

    return db_nota_final

# Actualizar una nota final por ID

def update_nota_final(db: Session, id_nota_final: int, nota_final: NotaFinalCreate):

    logger.info(f"Actualizando nota final ID: {id_nota_final}")

    db_nota_final = db.query(Notas_Finales).filter(Notas_Finales.id_nota_final == id_nota_final).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_nota_final.__dict__, default=str)}")

    if db_nota_final:
        db_nota_final.fk_usuario_id = nota_final.fk_usuario_id
        db_nota_final.fk_asignatura_id = nota_final.fk_asignatura_id
        db_nota_final.fk_trimestre_id = nota_final.fk_trimestre_id
        db_nota_final.nota_promedio = nota_final.nota_promedio
        db_nota_final.porcentaje_asistencia = nota_final.porcentaje_asistencia
        db_nota_final.estado_aprobacion = nota_final.estado_aprobacion
        db.commit()
        db.refresh(db_nota_final)

    logger.info(f"Nota final ID: {id_nota_final} actualizada exitosamente")

    return db_nota_final

# Actualizar la puntuacion de una nota final por ID

def update_promedio_nota_final(db: Session, id_nota_final: int, nota_final: NotaFinalPromedioUpdate):

    logger.info(f"Actualizando el promedio de la nota final ID: {id_nota_final}")

    db_nota_final = db.query(Notas_Finales).filter(Notas_Finales.id_nota_final == id_nota_final).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_nota_final.__dict__, default=str)}")

    if db_nota_final:
        db_nota_final.nota_promedio = nota_final.nota_promedio
        db_nota_final.estado_aprobacion = nota_final.estado_aprobacion
        db.commit()
        db.refresh(db_nota_final)

    logger.info(f"El promedio de la nota final ID: {id_nota_final} ha sido actualizada exitosamente")

    return db_nota_final

# Actualizar el estatus de una nota final por ID (Soft-Delete)

def update_estatus_nota_final(db: Session, id_nota_final: int, nota_final: NotaFinalEstatusUpdate):

    logger.info(f"Actualizando el estatus de la nota final ID: {id_nota_final}")

    db_nota_final = db.query(Notas_Finales).filter(Notas_Finales.id_nota_final == id_nota_final).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_nota_final.__dict__, default=str)}")

    if db_nota_final:
        db_nota_final.estatus_nota_final = nota_final.estatus_nota_final
        db.commit()
        db.refresh(db_nota_final)

    logger.info(f"El estatus de la nota final ID: {id_nota_final} ha sido actualizado exitosamente")

    return db_nota_final

# Eliminar una nota final por ID

def delete_nota_final(db: Session, id_nota_final: int):

    logger.warning(f"ELIMINANDO nota final ID: {id_nota_final} - Esta acción es permanente")

    db_nota_final = db.query(Notas_Finales).filter(Notas_Finales.id_nota_final == id_nota_final).first()
    db.delete(db_nota_final)
    db.commit()

    logger.warning(f"Nota final ID: {id_nota_final} eliminada permanentemente")

    return db_nota_final