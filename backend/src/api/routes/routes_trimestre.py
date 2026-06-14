from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_trimestre as trimestre_crud
from backend.src.schemas import schemas_trimestre as trimestre_schemas

router = APIRouter()

# Obtener trimestres, sea todos, y por ID

@router.get('/', response_model=List[trimestre_schemas.Trimestre])
def read_trimestres(db: Session = Depends(get_db)):
    return trimestre_crud.get_trimestres(db)

@router.get('/{id_trimestre}', response_model=trimestre_schemas.Trimestre)
def read_trimestre_por_id(id_trimestre: int, db: Session = Depends(get_db)):
    db_trimestre = trimestre_crud.get_trimestre_por_id(db, id_trimestre=id_trimestre)
    if db_trimestre is None:
        raise HTTPException(status_code=404, detail='Trimestre no encontrado')
    return db_trimestre

# Registrar un trimestre nuevo

@router.post('/create', response_model=trimestre_schemas.Trimestre)
def create_trimestre(trimestre: trimestre_schemas.TrimestreCreate, db: Session = Depends(get_db)):
    db_trimestre = trimestre_crud.get_trimestre_por_nombre(db, nombre=trimestre.nombre_trimestre)
    if db_trimestre:
        raise HTTPException(status_code=400, detail='Trimestre ya existente')
    return trimestre_crud.create_trimestre(db=db, trimestre=trimestre)

# Actualizar un trimestre registrado, por ID. Y actualizar tambien el estatus del trimestre (Soft-Delete)

@router.put('/update/{id_trimestre}', response_model=trimestre_schemas.Trimestre)
def update_trimestre(id_trimestre: int, trimestre: trimestre_schemas.TrimestreCreate, db: Session = Depends(get_db)):
    db_trimestre = trimestre_crud.get_trimestre_por_id(db, id_trimestre=id_trimestre)
    if db_trimestre is None:
        raise HTTPException(status_code=404, detail='Trimestre no encontrado')
    return trimestre_crud.update_trimestre(db=db, id_trimestre=id_trimestre, trimestre=trimestre)

@router.put('/update_status/{id_trimestre}', response_model=trimestre_schemas.Trimestre)
def update_estatus_trimestre(id_trimestre: int, trimestre: trimestre_schemas.TrimestreEstatusUpdate, db: Session = Depends(get_db)):
    db_trimestre = trimestre_crud.get_trimestre_por_id(db, id_trimestre=id_trimestre)
    if db_trimestre is None:
        raise HTTPException(status_code=404, detail='Trimestre no encontrado')
    return trimestre_crud.update_estatus_trimestre(db=db, id_trimestre=id_trimestre, trimestre=trimestre)

# Eliminar un trimestre registrado, por ID

@router.delete('/delete/{id_trimestre}', response_model=trimestre_schemas.Trimestre)
def delete_trimestre(id_trimestre: int, db: Session = Depends(get_db)):
    db_trimestre = trimestre_crud.get_trimestre_por_id(db, id_trimestre=id_trimestre)
    if db_trimestre is None:
        raise HTTPException(status_code=404, detail='Trimestre no encontrado')
    return trimestre_crud.delete_trimestre(db=db, id_trimestre=id_trimestre)