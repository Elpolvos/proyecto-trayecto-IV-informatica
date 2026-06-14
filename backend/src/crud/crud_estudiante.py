from sqlalchemy.orm import Session
from backend.src.models.models_estudiante import Estudiantes
from backend.src.schemas.schemas_estudiante import EstudianteCreate, EstudianteEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los estudiantes

def get_estudiantes(db: Session):

    logger.info(f"Todos los estudiantes obtenidos exitosamente")    

    return db.query(Estudiantes).all()

# Obtener un estudiante por ID

def get_estudiante_por_id(db: Session, id_estudiante: int):

    logger.info(f"Estudiante ID: {Estudiantes.id_estudiante} obtenido exitosamente")    

    return db.query(Estudiantes).filter(Estudiantes.id_estudiante == id_estudiante).first()

# Obtener un estudiante por DNI

def get_estudiante_por_dni(db: Session, dni_estudiante: str):

    logger.info(f"Estudiante DNI: {Estudiantes.dni_estudiante} obtenido exitosamente")    

    return db.query(Estudiantes).filter(Estudiantes.dni_estudiante == dni_estudiante).first()

# Crear un estudiante

def create_estudiante(db: Session, estudiante: EstudianteCreate):

    logger.info(f"Creando nuevo estudiante con DNI: {estudiante.dni_estudiante}")

    db_estudiante = Estudiantes(dni_estudiante = estudiante.dni_estudiante,
                                apellido_estudiante = estudiante.apellido_estudiante,
                                nombre_estudiante = estudiante.nombre_estudiante,
                                fechanacimiento_estudiante = estudiante.fechanacimiento_estudiante,
                                sexo_estudiante = estudiante.sexo_estudiante,
                                direccion_estudiante = estudiante.direccion_estudiante,
                                telefono_estudiante = estudiante.telefono_estudiante,
                                email_estudiante = estudiante.email_estudiante,
                                contrasena_estudiante = estudiante.contrasena_estudiante
                                )
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)

    logger.info(f"Estudiante creado exitosamente - ID: {db_estudiante.id_estudiante}")    

    return db_estudiante

# Actualizar un estudiante por ID

def update_estudiante(db: Session, id_estudiante: int, estudiante: EstudianteCreate):

    logger.info(f"Actualizando estudiante ID: {id_estudiante}")

    db_estudiante = db.query(Estudiantes).filter(Estudiantes.id_estudiante == id_estudiante).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_estudiante.__dict__, default=str)}")

    if db_estudiante:
        db_estudiante.dni_estudiante = estudiante.dni_estudiante
        db_estudiante.apellido_estudiante = estudiante.apellido_estudiante
        db_estudiante.nombre_estudiante = estudiante.nombre_estudiante
        db_estudiante.fechanacimiento_estudiante = estudiante.fechanacimiento_estudiante
        db_estudiante.sexo_estudiante = estudiante.sexo_estudiante
        db_estudiante.direccion_estudiante = estudiante.direccion_estudiante
        db_estudiante.telefono_estudiante = estudiante.telefono_estudiante
        db_estudiante.telefono_estudiante = estudiante.telefono_estudiante
        db.commit()
        db.refresh(db_estudiante)

    logger.info(f"Estudiante ID: {id_estudiante} actualizado exitosamente")

    return db_estudiante

# Actualizar el estatus de un estudiante por ID (Soft-Delete)

def update_estatus_estudiante(db: Session, id_estudiante: int, estudiante: EstudianteEstatusUpdate):

    logger.info(f"Actualizando el estatus del estudiante ID: {id_estudiante}")

    db_estudiante = db.query(Estudiantes).filter(Estudiantes.id_estudiante == id_estudiante).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_estudiante.__dict__, default=str)}")

    if db_estudiante:
        db_estudiante.estatus_estudiante = estudiante.estatus_estudiante
        db.commit()
        db.refresh(db_estudiante)
    
    logger.info(f"El estatus del estudiante ID: {id_estudiante} ha sido actualizado exitosamente")

    return db_estudiante

# Eliminar un estudiante por ID

def delete_estudiante(db: Session, id_estudiante: int):

    logger.warning(f"ELIMINANDO estudiante ID: {id_estudiante} - Esta acción es permanente")

    db_estudiante = db.query(Estudiantes).filter(Estudiantes.id_estudiante == id_estudiante).first()
    db.delete(db_estudiante)
    db.commit()
    
    logger.warning(f"Estudiante ID: {id_estudiante} eliminado permanentemente")
    
    return db_estudiante