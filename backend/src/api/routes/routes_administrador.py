from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_administrador as administrador_crud
from backend.src.schemas import schemas_administrador as administrador_schemas

router = APIRouter()

# Obtener administradores, sea todos, por ID o por DNI

@router.get('/', response_model=List[administrador_schemas.Administrador])
def read_administradores(db: Session = Depends(get_db)):
    return administrador_crud.get_administradores(db)

@router.get('/{id_admin}', response_model=administrador_schemas.Administrador)
def read_administrador_por_id(id_admin: int, db: Session = Depends(get_db)):
    db_administrador = administrador_crud.get_administrador_por_id(db, id_admin=id_admin)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail='Administrador no encontrado')
    return db_administrador

@router.get('/dni/{dni_admin}', response_model=administrador_schemas.Administrador)
def read_administrador_por_dni(dni_admin: str, db: Session = Depends(get_db)):
    db_administrador = administrador_crud.get_administrador_por_dni(db, dni_admin=dni_admin)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail='Administrador no encontrado')
    return db_administrador

# Registrar un administrador nuevo

@router.post('/create', response_model=administrador_schemas.Administrador)
def create_administrador(administrador: administrador_schemas.AdministradorCreate, db: Session = Depends(get_db)):
    db_administrador = administrador_crud.get_administrador_por_dni(db, dni_admin=administrador.dni_administrador)
    if db_administrador:
        raise HTTPException(status_code=400, detail='Administrador ya existente')
    return administrador_crud.create_administrador(db=db, administrador=administrador)

# Actualizar un administrador registrado, por ID. Y actualizar tambien el estatus del estudiante (Soft-Delete)

@router.put('/update/{id_admin}',response_model=administrador_schemas.Administrador)
def update_administrador(id_admin: int, admin: administrador_schemas.AdministradorCreate, db: Session = Depends(get_db)):
    db_administrador = administrador_crud.get_administrador_por_id(db, id_admin=id_admin)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail='Administrador no encontrado')
    return administrador_crud.update_administrador(db=db, id_admin=id_admin, admin=admin)

@router.put('/update_estatus/{id_admin}',response_model=administrador_schemas.Administrador)
def update_estatus_administrador(id_admin: int, admin: administrador_schemas.AdministradorEstatusUpdate, db: Session = Depends(get_db)):
    db_administrador = administrador_crud.get_administrador_por_id(db, id_admin=id_admin)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail='Administrador no encontrado')
    return administrador_crud.update_estatus_administrador(db=db, id_admin=id_admin, admin=admin)

# Eliminar un administrador registrado, por ID

@router.delete('/delete/{id_admin}', response_model=administrador_schemas.Administrador)
def delete_administrador(id_admin: int, db: Session = Depends(get_db)):
    db_administrador = administrador_crud.get_administrador_por_id(db, id_admin=id_admin)
    if db_administrador is None:
        raise HTTPException(status_code=404, detail='Administrador no encontrado')
    return administrador_crud.delete_administrador(db=db, id_admin=id_admin)