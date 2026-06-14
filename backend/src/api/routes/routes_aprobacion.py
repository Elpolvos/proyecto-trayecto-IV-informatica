from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_aprobacion as aprobacion_crud
from backend.src.schemas import schemas_aprobacion as aprobacion_schemas

router = APIRouter()

# Obtener estados de aprobacion, sean todos, o por ID

@router.get('/', response_model=List[aprobacion_schemas.Aprobacion])
def read_aprobaciones(db: Session = Depends(get_db)):
    return aprobacion_crud.get_aprobaciones(db)

@router.get('/{id_estado_aprobacion}', response_model=aprobacion_schemas.Aprobacion)
def read_aprobacion_por_id(id_estado_aprobacion: int, db: Session = Depends(get_db)):
    db_estado_aprobacion = aprobacion_crud.get_aprobacion_por_id(db, id_estado_aprobacion=id_estado_aprobacion)
    if db_estado_aprobacion is None:
        raise HTTPException(status_code=404, detail='Estado de aprobacion no encontrado')
    return db_estado_aprobacion

# Registrar un estado de aprobacion nuevo

@router.post('/create', response_model=aprobacion_schemas.Aprobacion)
def create_aprobacion(aprobacion: aprobacion_schemas.AprobacionCreate, db: Session = Depends(get_db)):
    db_estado_aprobacion = aprobacion_crud.get_aprobacion_por_tipo(db, estado_aprobacion=aprobacion.estado_aprobacion)
    if db_estado_aprobacion:
        raise HTTPException(status_code=400, detail='Estado de aprobacion ya existente')
    return aprobacion_crud.create_aprobacion(db=db, aprobacion=aprobacion)

# Actualizar un estado de aprobacion registrado, por ID. Y actualizar tambien el estatus del estado de aprobacion (Soft-Delete)

@router.put('/update/{id_estado_aprobacion}', response_model=aprobacion_schemas.Aprobacion)
def update_aprobacion(id_estado_aprobacion: int, aprobacion: aprobacion_schemas.AprobacionCreate, db: Session = Depends(get_db)):
    db_estado_aprobacion = aprobacion_crud.get_aprobacion_por_id(db, id_estado_aprobacion=id_estado_aprobacion)
    if db_estado_aprobacion is None:
        raise HTTPException(status_code=404, detail='Estado de aprobacion no encontrado')
    return aprobacion_crud.update_aprobacion(db=db, id_estado_aprobacion=id_estado_aprobacion, aprobacion=aprobacion)

@router.put('/update_status/{id_estado_aprobacion}', response_model=aprobacion_schemas.Aprobacion)
def update_estatus_aprobacion(id_estado_aprobacion: int, aprobacion: aprobacion_schemas.AprobacionEstatusUpdate, db: Session = Depends(get_db)):
    db_estado_aprobacion = aprobacion_crud.get_aprobacion_por_id(db, id_estado_aprobacion=id_estado_aprobacion)
    if db_estado_aprobacion is None:
        raise HTTPException(status_code=404, detail='Estado de aprobacion no encontrado')
    return aprobacion_crud.update_estatus_aprobacion(db=db, id_estado_aprobacion=id_estado_aprobacion, aprobacion=aprobacion)

# Eliminar un estado de aprobacion registrado, por ID

@router.delete('/delete/{id_estado_aprobacion}', response_model=aprobacion_schemas.Aprobacion)
def delete_aprobacion(id_estado_aprobacion: int, db: Session = Depends(get_db)):
    db_estado_aprobacion = aprobacion_crud.get_aprobacion_por_id(db, id_estado_aprobacion=id_estado_aprobacion)
    if db_estado_aprobacion is None:
        raise HTTPException(status_code=404, detail='Estado de aprobacion no encontrado')
    return aprobacion_crud.delete_aprobacion(db=db, id_estado_aprobacion=id_estado_aprobacion)