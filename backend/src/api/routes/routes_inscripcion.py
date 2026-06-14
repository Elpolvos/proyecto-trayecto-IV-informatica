from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_inscripcion as inscripcion_crud
from backend.src.schemas import schemas_inscripcion as inscripcion_schemas

router = APIRouter()

# Obtener inscripciones, sea todos, por ID, por usuario-estudiante, por seccion o por año escolar

@router.get('/', response_model=List[inscripcion_schemas.Inscripcion])
def read_inscripciones(db: Session = Depends(get_db)):
    return inscripcion_crud.get_inscripciones(db)

@router.get('/{id_inscripcion}', response_model=inscripcion_schemas.Inscripcion)
def read_inscripcion_por_id(id_inscripcion: int, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_crud.get_inscripcion_por_id(db, id_inscripcion=id_inscripcion)
    if db_inscripcion is None:
        raise HTTPException(status_code=404, detail='Inscripción no encontrada')
    return db_inscripcion

@router.get('/estudiante/{fk_usuario_id}', response_model=List[inscripcion_schemas.Inscripcion])
def read_inscripciones_por_estudiante(fk_usuario_id: int, db: Session = Depends(get_db)):
    return inscripcion_crud.get_inscripciones_por_estudiante(db, fk_usuario_id=fk_usuario_id)

@router.get('/seccion/{fk_seccion_id}', response_model=List[inscripcion_schemas.Inscripcion])
def read_inscripciones_por_seccion(fk_seccion_id: int, db: Session = Depends(get_db)):
    return inscripcion_crud.get_inscripciones_por_seccion(db, fk_seccion_id=fk_seccion_id)

@router.get('/anio/{anio_escolar}', response_model=List[inscripcion_schemas.Inscripcion])
def read_inscripciones_por_anio(anio_escolar: int, db: Session = Depends(get_db)):
    return inscripcion_crud.get_inscripciones_por_anio_escolar(db, anio_escolar=anio_escolar)

# Registrar una inscripcion nueva

@router.post('/create', response_model=inscripcion_schemas.Inscripcion)
def create_inscripcion(inscripcion: inscripcion_schemas.InscripcionCreate, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_crud.get_inscripcion_por_estudiante_anio(
        db,
        fk_usuario_id=inscripcion.fk_usuario_id,
        anio_escolar=inscripcion.anio_escolar
    )
    if db_inscripcion:
        raise HTTPException(status_code=400, detail='El estudiante ya está inscrito para este año escolar')
    return inscripcion_crud.create_inscripcion(db=db, inscripcion=inscripcion)

# Actualizar una inscripcion registrada, por ID. Y actualizar tambien el estatus de la inscripcion (Soft-Delete)

@router.put('/update/{id_inscripcion}', response_model=inscripcion_schemas.Inscripcion)
def update_inscripcion(id_inscripcion: int, inscripcion: inscripcion_schemas.InscripcionCreate, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_crud.get_inscripcion_por_id(db, id_inscripcion=id_inscripcion)
    if db_inscripcion is None:
        raise HTTPException(status_code=404, detail='Inscripción no encontrada')
    return inscripcion_crud.update_inscripcion(db=db, id_inscripcion=id_inscripcion, inscripcion=inscripcion)

@router.put('/update_status/{id_inscripcion}', response_model=inscripcion_schemas.Inscripcion)
def update_estatus_inscripcion(id_inscripcion: int, inscripcion: inscripcion_schemas.InscripcionEstatusUpdate, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_crud.get_inscripcion_por_id(db, id_inscripcion=id_inscripcion)
    if db_inscripcion is None:
        raise HTTPException(status_code=404, detail='Inscripción no encontrada')
    return inscripcion_crud.update_estatus_inscripcion(db=db, id_inscripcion=id_inscripcion, inscripcion=inscripcion)

# Eliminar una inscripcion registrada, por ID

@router.delete('/delete/{id_inscripcion}', response_model=inscripcion_schemas.Inscripcion)
def delete_inscripcion(id_inscripcion: int, db: Session = Depends(get_db)):
    db_inscripcion = inscripcion_crud.get_inscripcion_por_id(db, id_inscripcion=id_inscripcion)
    if db_inscripcion is None:
        raise HTTPException(status_code=404, detail='Inscripción no encontrada')
    return inscripcion_crud.delete_inscripcion(db=db, id_inscripcion=id_inscripcion)