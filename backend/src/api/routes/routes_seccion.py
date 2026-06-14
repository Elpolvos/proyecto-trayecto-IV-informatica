from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_seccion as seccion_crud
from backend.src.schemas import schemas_seccion as seccion_schemas

router = APIRouter()

# Obtener secciones, sea todos, y por ID

@router.get('/', response_model=List[seccion_schemas.Seccion])
def read_secciones(db: Session = Depends(get_db)):
    return seccion_crud.get_secciones(db)

@router.get('/{id_seccion}', response_model=seccion_schemas.Seccion)
def read_seccion_por_id(id_seccion: int, db: Session = Depends(get_db)):
    db_seccion = seccion_crud.get_seccion_por_id(db, id_seccion=id_seccion)
    if db_seccion is None:
        raise HTTPException(status_code=404, detail='Sección no encontrada')
    return db_seccion

# Registrar una seccion nueva

@router.post('/create', response_model=seccion_schemas.Seccion)
def create_seccion(seccion: seccion_schemas.SeccionCreate, db: Session = Depends(get_db)):
    db_seccion = seccion_crud.get_seccion_por_descripcion(db, descripcion=seccion.descripcion_seccion)
    if db_seccion:
        raise HTTPException(status_code=400, detail='Sección ya existente')
    return seccion_crud.create_seccion(db=db, seccion=seccion)

# Actualizar una seccion registrada, por ID. Y actualizar tambien el estatus de la seccion (Soft-Delete)

@router.put('/update/{id_seccion}', response_model=seccion_schemas.Seccion)
def update_seccion(id_seccion: int, seccion: seccion_schemas.SeccionCreate, db: Session = Depends(get_db)):
    db_seccion = seccion_crud.get_seccion_por_id(db, id_seccion=id_seccion)
    if db_seccion is None:
        raise HTTPException(status_code=404, detail='Sección no encontrada')
    return seccion_crud.update_seccion(db=db, id_seccion=id_seccion, seccion=seccion)

@router.put('/update_status/{id_seccion}', response_model=seccion_schemas.Seccion)
def update_estatus_seccion(id_seccion: int, seccion: seccion_schemas.SeccionEstatusUpdate, db: Session = Depends(get_db)):
    db_seccion = seccion_crud.get_seccion_por_id(db, id_seccion=id_seccion)
    if db_seccion is None:
        raise HTTPException(status_code=404, detail='Sección no encontrada')
    return seccion_crud.update_estatus_seccion(db=db, id_seccion=id_seccion, seccion=seccion)

# Eliminar una seccion registrada, por ID

@router.delete('/delete/{id_seccion}', response_model=seccion_schemas.Seccion)
def delete_seccion(id_seccion: int, db: Session = Depends(get_db)):
    db_seccion = seccion_crud.get_seccion_por_id(db, id_seccion=id_seccion)
    if db_seccion is None:
        raise HTTPException(status_code=404, detail='Sección no encontrada')
    return seccion_crud.delete_seccion(db=db, id_seccion=id_seccion)