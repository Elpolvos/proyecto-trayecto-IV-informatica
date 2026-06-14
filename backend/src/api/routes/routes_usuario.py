from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_usuario as usuario_crud
from backend.src.schemas import schemas_usuario as usuario_schemas

router = APIRouter()

# Obtener usuarios, sea todos, por ID, por email o por DNI

@router.get('/', response_model=List[usuario_schemas.Usuario])
def read_usuarios(db: Session = Depends(get_db)):
    return usuario_crud.get_usuarios(db)

@router.get('/{id_usuario}', response_model=usuario_schemas.Usuario)
def read_usuario_por_id(id_usuario: int, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_id(db, id_usuario=id_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return db_usuario

@router.get('/email/{email_usuario}', response_model=usuario_schemas.Usuario)
def read_usuario_por_email(email_usuario: str, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_email(db, email_usuario=email_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return db_usuario

@router.get('/dni/{dni_usuario}', response_model=usuario_schemas.Usuario)
def read_usuario_por_dni(dni_usuario: str, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_dni(db, dni_usuario=dni_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return db_usuario

# Registrar un usuario nuevo

@router.post('/create', response_model=usuario_schemas.Usuario)
def create_usuario(usuario: usuario_schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_email(db, email=usuario.email_usuario)
    if db_usuario:
        raise HTTPException(status_code=400, detail='Usuario ya existente')
    return usuario_crud.create_usuario(db=db, usuario=usuario)

# Actualizar un usuario registrado, por ID. Y actualizar tambien el estatus del usuario (Soft-Delete)

@router.put('/update/{id_usuario}', response_model=usuario_schemas.Usuario)
def update_usuario(id_usuario: int, usuario: usuario_schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_id(db, id_usuario=id_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario_crud.update_usuario(db=db, id_usuario=id_usuario, usuario=usuario)

@router.put('/update_status/{id_usuario}', response_model=usuario_schemas.Usuario)
def update_estatus_usuario(id_usuario: int, usuario: usuario_schemas.UsuarioEstatusUpdate, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_id(db, id_usuario=id_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario_crud.update_estatus_usuario(db=db, id_usuario=id_usuario, usuario=usuario)

# Eliminar un usuario registrado, por ID

@router.delete('/delete/{id_usuario}', response_model=usuario_schemas.Usuario)
def delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    db_usuario = usuario_crud.get_usuario_por_id(db, id_usuario=id_usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario_crud.delete_usuario(db=db, id_usuario=id_usuario)