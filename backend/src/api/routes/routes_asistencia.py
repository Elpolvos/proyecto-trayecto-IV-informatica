from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from backend.src.api.deps import get_db
from backend.src.crud import crud_asistencia as asistencia_crud
from backend.src.schemas import schemas_asistencia as asistencia_schemas

router = APIRouter()

# Obtener asistencias, sea todos, por ID, por usuario-estudiante, por asignatura o por fecha

@router.get('/', response_model=List[asistencia_schemas.Asistencia])
def read_asistencias(db: Session = Depends(get_db)):
    return asistencia_crud.get_asistencias(db)

@router.get('/{id_asistencia}', response_model=asistencia_schemas.Asistencia)
def read_asistencia_por_id(id_asistencia: int, db: Session = Depends(get_db)):
    db_asistencia = asistencia_crud.get_asistencia_por_id(db, id_asistencia=id_asistencia)
    if db_asistencia is None:
        raise HTTPException(status_code=404, detail='Asistencia no encontrada')
    return db_asistencia

@router.get('/estudiante/{fk_usuario_id}', response_model=List[asistencia_schemas.Asistencia])
def read_asistencias_por_estudiante(fk_usuario_id: int, db: Session = Depends(get_db)):
    return asistencia_crud.get_asistencias_por_estudiante(db, fk_usuario_id=fk_usuario_id)

@router.get('/asignatura/{fk_asignatura_id}', response_model=List[asistencia_schemas.Asistencia])
def read_asistencias_por_asignatura(fk_asignatura_id: int, db: Session = Depends(get_db)):
    return asistencia_crud.get_asistencias_por_asignatura(db, fk_asignatura_id=fk_asignatura_id)

@router.get('/fecha/{fecha_asistencia}', response_model=List[asistencia_schemas.Asistencia])
def read_asistencias_por_fecha(fecha_asistencia: date, db: Session = Depends(get_db)):
    return asistencia_crud.get_asistencias_por_fecha(db, fecha=fecha_asistencia)

# Registrar una asistencia nueva

@router.post('/create', response_model=asistencia_schemas.Asistencia)
def create_asistencia(asistencia: asistencia_schemas.AsistenciaCreate, db: Session = Depends(get_db)):
    db_asistencia = asistencia_crud.get_asistencia_por_estudiante_asignatura_fecha(
        db,
        fk_usuario_id=asistencia.fk_usuario_id,
        fk_asignatura_id=asistencia.fk_asignatura_id,
        fecha=asistencia.fecha_asistencia
    )
    if db_asistencia:
        raise HTTPException(status_code=400, detail='Ya existe un registro de asistencia para este estudiante, asignatura y fecha')
    return asistencia_crud.create_asistencia(db=db, asistencia=asistencia)

# Actualizar una asistencia registrada, por ID. Además, actualizar el presente de la asistencia, tambien por ID. Y actualizar tambien el estatus de la asistencia (Soft-Delete)

@router.put('/update/{id_asistencia}', response_model=asistencia_schemas.Asistencia)
def update_asistencia(id_asistencia: int, asistencia: asistencia_schemas.AsistenciaCreate, db: Session = Depends(get_db)):
    db_asistencia = asistencia_crud.get_asistencia_por_id(db, id_asistencia=id_asistencia)
    if db_asistencia is None:
        raise HTTPException(status_code=404, detail='Asistencia no encontrada')
    return asistencia_crud.update_asistencia(db=db, id_asistencia=id_asistencia, asistencia=asistencia)

@router.patch('/update_presente/{id_asistencia}', response_model=asistencia_schemas.Asistencia)
def update_presente_asistencia(id_asistencia: int, asistencia: asistencia_schemas.AsistenciaPresenteUpdate, db: Session = Depends(get_db)):
    db_asistencia = asistencia_crud.get_asistencia_por_id(db, id_asistencia=id_asistencia)
    if db_asistencia is None:
        raise HTTPException(status_code=404, detail='Asistencia no encontrada')
    return asistencia_crud.update_presente_asistencia(db=db, id_asistencia=id_asistencia, asistencia=asistencia)

@router.put('/update_status/{id_asistencia}', response_model=asistencia_schemas.Asistencia)
def update_estatus_asistencia(id_asistencia: int, asistencia: asistencia_schemas.AsistenciaEstatusUpdate, db: Session = Depends(get_db)):
    db_asistencia = asistencia_crud.get_asistencia_por_id(db, id_asistencia=id_asistencia)
    if db_asistencia is None:
        raise HTTPException(status_code=404, detail='Asistencia no encontrada')
    return asistencia_crud.update_estatus_asistencia(db=db, id_asistencia=id_asistencia, asistencia=asistencia)

# Eliminar una asistencia registrada, por ID

@router.delete('/delete/{id_asistencia}', response_model=asistencia_schemas.Asistencia)
def delete_asistencia(id_asistencia: int, db: Session = Depends(get_db)):
    db_asistencia = asistencia_crud.get_asistencia_por_id(db, id_asistencia=id_asistencia)
    if db_asistencia is None:
        raise HTTPException(status_code=404, detail='Asistencia no encontrada')
    return asistencia_crud.delete_asistencia(db=db, id_asistencia=id_asistencia)