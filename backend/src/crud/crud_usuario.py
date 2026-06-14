from sqlalchemy.orm import Session
from backend.src.models.models_usuario import Usuarios
from backend.src.schemas.schemas_usuario import UsuarioCreate, UsuarioEstatusUpdate

from backend.src.core.logging import logger
import json

# Obtener todos los usuarios

def get_usuarios(db: Session):

    logger.info(f"Todos los usuarios obtenidos exitosamente")    

    return db.query(Usuarios).all()

# Obtener un usuario por ID

def get_usuario_por_id(db: Session, id_usuario: int):

    logger.info(f"Usuario ID: {Usuarios.id_usuario} obtenido exitosamente")    

    return db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()

# Obtener un usuario por email

def get_usuario_por_email(db: Session, email: str):

    logger.info(f"Usuario dueño del email: {Usuarios.email_usuario} obtenido exitosamente")    

    return db.query(Usuarios).filter(Usuarios.email_usuario == email).first()

# Obtener un usuario por DNI

def get_usuario_por_dni(db: Session, dni_usuario: str):

    logger.info(f"Usuario dueño del DNI: {Usuarios.dni_usuario} obtenido exitosamente")    

    return db.query(Usuarios).filter(Usuarios.dni_usuario == dni_usuario).first()

# Crear un usuario

def create_usuario(db: Session, usuario: UsuarioCreate):

    logger.info(f"Creando nuevo usuario con email: {usuario.email_usuario}")

    db_usuario = Usuarios(fk_rol_id = usuario.fk_rol_id,
                          dni_usuario = usuario.dni_usuario,
                          apellido_usuario = usuario.apellido_usuario,
                          nombre_usuario = usuario.nombre_usuario,
                          fechanacimiento_usuario = usuario.fechanacimiento_usuario,
                          sexo_usuario = usuario.sexo_usuario,
                          direccion_usuario = usuario.direccion_usuario,
                          telefono_usuario = usuario.telefono_usuario,
                          email_usuario = usuario.email_usuario,
                          contrasena_usuario = usuario.contrasena_usuario,
                          fecha_registro = usuario.fecha_registro,
                          )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    logger.info(f"Usuario creado exitosamente - ID: {db_usuario.id_usuario}")    

    return db_usuario

# Actualizar un usuario por ID

def update_usuario(db: Session, id_usuario: int, usuario: UsuarioCreate):

    logger.info(f"Actualizando usuario ID: {id_usuario}")

    db_usuario = db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_usuario.__dict__, default=str)}")

    if db_usuario:
        db_usuario.fk_rol_id = usuario.fk_rol_id
        db_usuario.dni_usuario = usuario.dni_usuario
        db_usuario.apellido_usuario = usuario.apellido_usuario
        db_usuario.nombre_usuario = usuario.nombre_usuario
        db_usuario.fechanacimiento_usuario = usuario.fechanacimiento_usuario
        db_usuario.sexo_usuario = usuario.sexo_usuario
        db_usuario.direccion_usuario = usuario.direccion_usuario
        db_usuario.telefono_usuario = usuario.telefono_usuario
        db_usuario.email_usuario = usuario.email_usuario
        db_usuario.contrasena_usuario = usuario.contrasena_usuario
        db_usuario.fecha_registro = usuario.fecha_registro
        db.commit()
        db.refresh(db_usuario)

    logger.info(f"Usuario ID: {id_usuario} actualizado exitosamente")

    return db_usuario

# Actualizar el estatus de un usuario por ID (Soft-Delete)

def update_estatus_usuario(db: Session, id_usuario: int, usuario: UsuarioEstatusUpdate):

    logger.info(f"Actualizando el estatus del usuario ID: {id_usuario}")

    db_usuario = db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()

    # Log de datos anteriores
    logger.debug(f"Datos anteriores: {json.dumps(db_usuario.__dict__, default=str)}")

    if db_usuario:
        db_usuario.estatus_usuario = usuario.estatus_usuario
        db.commit()
        db.refresh(db_usuario)
    
    logger.info(f"El estatus del usuario ID: {id_usuario} ha sido actualizado exitosamente")

    return db_usuario

# Eliminar un usuario por ID

def delete_usuario(db: Session, id_usuario: int):

    logger.warning(f"ELIMINANDO usuario ID: {id_usuario} - Esta acción es permanente")

    db_usuario = db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()
    db.delete(db_usuario)
    db.commit()
    
    logger.warning(f"Usuario ID: {id_usuario} eliminado permanentemente")
    
    return db_usuario