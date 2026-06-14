from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_estudiante as estudiante_crud
from backend.src.schemas import schemas_estudiante as estudiante_schemas

router = APIRouter()

# Obtener estudiantes, sea todos, por ID o por DNI

@router.get('/', response_model=List[estudiante_schemas.Estudiante])
def read_estudiantes(db: Session = Depends(get_db)):
    return estudiante_crud.get_estudiantes(db)

@router.get('/{id_estudiante}', response_model=estudiante_schemas.Estudiante)
def read_estudiante_por_id(id_estudiante: int, db: Session = Depends(get_db)):
    db_estudiante = estudiante_crud.get_estudiante_por_id(db, id_estudiante=id_estudiante)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail='Estudiante no encontrado')
    return db_estudiante

@router.get('/dni/{dni_estudiante}', response_model=estudiante_schemas.Estudiante)
def read_estudiante_por_dni(dni_estudiante: str, db: Session = Depends(get_db)):
    db_estudiante = estudiante_crud.get_estudiante_por_dni(db, dni_estudiante=dni_estudiante)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail='Estudiante no encontrado')
    return db_estudiante

# Registrar un estudiante nuevo

@router.post('/create', response_model=estudiante_schemas.Estudiante)
def create_estudiante(estudiante: estudiante_schemas.EstudianteCreate, db: Session = Depends(get_db)):
    db_estudiante = estudiante_crud.get_estudiante_por_dni(db, dni_estudiante=estudiante.dni_estudiante)
    if db_estudiante:
        raise HTTPException(status_code=400, detail='Estudiante ya existente')
    return estudiante_crud.create_estudiante(db=db, estudiante=estudiante)

# Actualizar un estudiante registrado, por ID. Y actualizar tambien el estatus del estudiante (Soft-Delete)

@router.put('/update/{id_estudiante}', response_model=estudiante_schemas.Estudiante)
def update_estudiante(id_estudiante: int, estudiante: estudiante_schemas.EstudianteCreate, db: Session = Depends(get_db)):
    db_estudiante = estudiante_crud.get_estudiante_por_id(db, id_estudiante=id_estudiante)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail='Estudiante no encontrado')
    return estudiante_crud.update_estudiante(db=db, id_estudiante=id_estudiante, estudiante=estudiante)

@router.put('/update_status/{id_estudiante}', response_model=estudiante_schemas.Estudiante)
def update_estatus_estudiante(id_estudiante: int, estudiante: estudiante_schemas.EstudianteEstatusUpdate, db: Session = Depends(get_db)):
    db_estudiante = estudiante_crud.get_estudiante_por_id(db, id_estudiante=id_estudiante)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail='Estudiante no encontrado')
    return estudiante_crud.update_estatus_estudiante(db=db, id_estudiante=id_estudiante, estudiante=estudiante)

# Eliminar un estudiante registrado, por ID

@router.delete('/delete/{id_estudiante}', response_model=estudiante_schemas.Estudiante)
def delete_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    db_estudiante = estudiante_crud.get_estudiante_por_id(db, id_estudiante=id_estudiante)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail='Estudiante no encontrado')
    return estudiante_crud.delete_estudiante(db=db, id_estudiante=id_estudiante)