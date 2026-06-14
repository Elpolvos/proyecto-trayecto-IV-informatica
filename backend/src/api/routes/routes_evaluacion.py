from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_evaluacion as evaluacion_crud
from backend.src.schemas import schemas_evaluacion as evaluacion_schemas

router = APIRouter()

# Obtener evaluaciones, sea todos, por ID, por asignatura o por trimestre

@router.get('/', response_model=List[evaluacion_schemas.Evaluacion])
def read_evaluaciones(db: Session = Depends(get_db)):
    return evaluacion_crud.get_evaluaciones(db)

@router.get('/{id_evaluacion}', response_model=evaluacion_schemas.Evaluacion)
def read_evaluacion_por_id(id_evaluacion: int, db: Session = Depends(get_db)):
    db_evaluacion = evaluacion_crud.get_evaluacion_por_id(db, id_evaluacion=id_evaluacion)
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail='Evaluación no encontrada')
    return db_evaluacion

@router.get('/asignatura/{fk_asignatura_id}', response_model=List[evaluacion_schemas.Evaluacion])
def read_evaluaciones_por_asignatura(fk_asignatura_id: int, db: Session = Depends(get_db)):
    return evaluacion_crud.get_evaluaciones_por_asignatura(db, fk_asignatura_id=fk_asignatura_id)

@router.get('/trimestre/{fk_trimestre_id}', response_model=List[evaluacion_schemas.Evaluacion])
def read_evaluaciones_por_trimestre(fk_trimestre_id: int, db: Session = Depends(get_db)):
    return evaluacion_crud.get_evaluaciones_por_trimestre(db, fk_trimestre_id=fk_trimestre_id)

# Registrar una evaluacion nueva

@router.post('/create', response_model=evaluacion_schemas.Evaluacion)
def create_evaluacion(evaluacion: evaluacion_schemas.EvaluacionCreate, db: Session = Depends(get_db)):
    return evaluacion_crud.create_evaluacion(db=db, evaluacion=evaluacion)

# Actualizar una evaluacion registrada, por ID. Y actualizar tambien el estatus de la evaluacion (Soft-Delete)

@router.put('/update/{id_evaluacion}', response_model=evaluacion_schemas.Evaluacion)
def update_evaluacion(id_evaluacion: int, evaluacion: evaluacion_schemas.EvaluacionCreate, db: Session = Depends(get_db)):
    db_evaluacion = evaluacion_crud.get_evaluacion_por_id(db, id_evaluacion=id_evaluacion)
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail='Evaluación no encontrada')
    return evaluacion_crud.update_evaluacion(db=db, id_evaluacion=id_evaluacion, evaluacion=evaluacion)

@router.put('/update_status/{id_evaluacion}', response_model=evaluacion_schemas.Evaluacion)
def update_estatus_evaluacion(id_evaluacion: int, evaluacion: evaluacion_schemas.EvaluacionEstatusUpdate, db: Session = Depends(get_db)):
    db_evaluacion = evaluacion_crud.get_evaluacion_por_id(db, id_evaluacion=id_evaluacion)
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail='Evaluación no encontrada')
    return evaluacion_crud.update_estatus_evaluacion(db=db, id_evaluacion=id_evaluacion, evaluacion=evaluacion)

# Eliminar una evaluacion registrada, por ID

@router.delete('/delete/{id_evaluacion}', response_model=evaluacion_schemas.Evaluacion)
def delete_evaluacion(id_evaluacion: int, db: Session = Depends(get_db)):
    db_evaluacion = evaluacion_crud.get_evaluacion_por_id(db, id_evaluacion=id_evaluacion)
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail='Evaluación no encontrada')
    return evaluacion_crud.delete_evaluacion(db=db, id_evaluacion=id_evaluacion)