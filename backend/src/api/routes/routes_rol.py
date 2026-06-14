from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_rol as rol_crud
from backend.src.schemas import schemas_rol as rol_schemas

router = APIRouter()

# Obtener roles, sea todos, y por ID

@router.get('/', response_model=List[rol_schemas.Rol])
def read_roles(db: Session = Depends(get_db)):
    return rol_crud.get_roles(db)

@router.get('/{id_rol}', response_model=rol_schemas.Rol)
def read_rol_por_id(id_rol: int, db: Session = Depends(get_db)):
    db_rol = rol_crud.get_rol_por_id(db, id_rol=id_rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
    return db_rol

# Registrar un rol nuevo

@router.post('/create', response_model=rol_schemas.Rol)
def create_rol(rol: rol_schemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = rol_crud.get_rol_por_tipo(db, tipo_rol=rol.tipo_rol)
    if db_rol:
        raise HTTPException(status_code=400, detail='Rol ya existente')
    return rol_crud.create_rol(db=db, rol=rol)

# Actualizar un rol registrado, por ID. Y actualizar tambien el estatus del rol (Soft-Delete)

@router.put('/update/{id_rol}', response_model=rol_schemas.Rol)
def update_rol(id_rol: int, rol: rol_schemas.RolCreate, db: Session = Depends(get_db)):
    db_rol = rol_crud.get_rol_por_id(db, id_rol=id_rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
    return rol_crud.update_rol(db=db, id_rol=id_rol, rol=rol)

@router.put('/update_status/{id_rol}', response_model=rol_schemas.Rol)
def update_estatus_rol(id_rol: int, rol: rol_schemas.RolEstatusUpdate, db: Session = Depends(get_db)):
    db_rol = rol_crud.get_rol_por_id(db, id_rol=id_rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
    return rol_crud.update_estatus_rol(db=db, id_rol=id_rol, rol=rol)

# Eliminar un rol registrado, por ID

@router.delete('/delete/{id_rol}', response_model=rol_schemas.Rol)
def delete_rol(id_rol: int, db: Session = Depends(get_db)):
    db_rol = rol_crud.get_rol_por_id(db, id_rol=id_rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
    return rol_crud.delete_rol(db=db, id_rol=id_rol)