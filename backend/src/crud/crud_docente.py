from sqlalchemy.orm import Session
from backend.src.models.models_docente import Docentes
from backend.src.schemas.schemas_docente import DocenteCreate, DocenteEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los docentes

def get_docentes(db: Session):

    logger.info(f"Todos los docentes obtenidos exitosamente.")

    return db.query(Docentes).all()

# Obtener un docente por ID

def get_docente_por_id(db: Session, id_docente: int):

    logger.info(f"Docente ID: {Docentes.id_docente} obtenido exitosamente")    

    return db.query(Docentes).filter(Docentes.id_docente == id_docente).first()

# Obtener un docente por DNI

def get_docente_por_dni(db: Session, dni_docente: str):

    logger.info(f"Docente DNI: {Docentes.dni_docente} obtenido exitosamente")    

    return db.query(Docentes).filter(Docentes.dni_docente == dni_docente).first()

# Crear un docente

def create_docente(db: Session, docente: DocenteCreate):

    logger.info(f"Creando nuevo docente con DNI: {docente.dni_docente}")

    db_docente = Docentes(dni_docente = docente.dni_docente,
                          apellido_docente = docente.apellido_docente,
                          nombre_docente = docente.nombre_docente,
                          fechanacimiento_docente = docente.fechanacimiento_docente,
                          sexo_docente = docente.sexo_docente,
                          direccion_docente = docente.direccion_docente,
                          telefono_docente = docente.telefono_docente,
                          email_docente = docente.email_docente,
                          contrasena_docente = docente.contrasena_docente
                          )
    db.add(db_docente)
    db.commit()
    db.refresh(db_docente)

    logger.info(f"Docente creado exitosamente - ID: {db_docente.id_docente}")    

    return db_docente

# Actualizar un docente por ID

def update_docente(db: Session, id_docente: int, docente: DocenteCreate):

    logger.info(f"Actualizando docente ID: {id_docente}")

    db_docente = db.query(Docentes).filter(Docentes.id_docente == id_docente).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_docente.__dict__, default=str)}")

    if db_docente:
        db_docente.dni_docente = docente.dni_docente
        db_docente.apellido_docente = docente.apellido_docente
        db_docente.nombre_docente = docente.nombre_docente
        db_docente.fechanacimiento_docente = docente.fechanacimiento_docente
        db_docente.sexo_docente = docente.sexo_docente
        db_docente.direccion_docente = docente.direccion_docente
        db_docente.telefono_docente = docente.telefono_docente
        db_docente.email_docente = docente.email_docente
        db_docente.contrasena_docente = docente.contrasena_docente
        db.commit()
        db.refresh(db_docente)

    logger.info(f"Docente ID: {id_docente} actualizado exitosamente")

    return db_docente

# Actualizar estatus de un docente por ID (Soft-Delete)

def update_estatus_docente(db: Session, id_docente: int, docente: DocenteEstatusUpdate):

    logger.info(f"Actualizando el estatus del docente ID: {id_docente}")

    db_docente = db.query(Docentes).filter(Docentes.id_docente == id_docente).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_docente.__dict__, default=str)}")

    if db_docente:
        db_docente.estatus_docente = docente.estatus_docente
        db.commit()
        db.refresh(db_docente)

    logger.info(f"El estatus del docente ID: {id_docente} ha sido actualizado exitosamente")

    return db_docente

# Eliminar un docente por ID

def delete_docente(db: Session, id_docente: int):

    logger.warning(f"ELIMINANDO docente ID: {id_docente} - Esta acción es permanente")

    db_docente = db.query(Docentes).filter(Docentes.id_docente == id_docente).first()
    db.delete(db_docente)
    db.commit()

    logger.warning(f"docente ID: {id_docente} eliminado permanentemente")

    return db_docente