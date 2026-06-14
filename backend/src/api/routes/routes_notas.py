from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_notas as nota_crud
from backend.src.schemas import schemas_notas as nota_schemas

router = APIRouter()

# Obtener notas, sea todos, por ID, por estudiante o por evaluacion

@router.get('/', response_model=List[nota_schemas.Nota])
def read_notas(db: Session = Depends(get_db)):
    return nota_crud.get_notas(db)

@router.get('/{id_nota}', response_model=nota_schemas.Nota)
def read_nota_por_id(id_nota: int, db: Session = Depends(get_db)):
    db_nota = nota_crud.get_nota_por_id(db, id_nota=id_nota)
    if db_nota is None:
        raise HTTPException(status_code=404, detail='Nota no encontrada')
    return db_nota

@router.get('/estudiante/{id_estudiante}', response_model=List[nota_schemas.Nota])
def read_notas_por_estudiante(id_estudiante: int, db: Session = Depends(get_db)):
    return nota_crud.get_notas_por_estudiante(db, id_estudiante=id_estudiante)

@router.get('/evaluacion/{id_evaluacion}', response_model=List[nota_schemas.Nota])
def read_notas_por_evaluacion(id_evaluacion: int, db: Session = Depends(get_db)):
    return nota_crud.get_notas_por_evaluacion(db, id_evaluacion=id_evaluacion)

# Registrar una nota nueva

@router.post('/create', response_model=nota_schemas.Nota)
def create_nota(nota: nota_schemas.NotaCreate, db: Session = Depends(get_db)):
    db_nota = nota_crud.get_nota_por_estudiante_evaluacion(db, id_estudiante=nota.id_estudiante, id_evaluacion=nota.id_evaluacion)
    if db_nota:
        raise HTTPException(status_code=400, detail='El estudiante ya tiene nota para esta evaluación')
    return nota_crud.create_nota(db=db, nota=nota)

# Actualizar una nota registrada, por ID. Además, actualizar la puntuación de la nota, tambien por ID. Y actualizar tambien el estatus de la nota (Soft-Delete)

@router.put('/update/{id_nota}', response_model=nota_schemas.Nota)
def update_nota(id_nota: int, nota: nota_schemas.NotaCreate, db: Session = Depends(get_db)):
    db_nota = nota_crud.get_nota_por_id(db, id_nota=id_nota)
    if db_nota is None:
        raise HTTPException(status_code=404, detail='Nota no encontrada')
    return nota_crud.update_nota(db=db, id_nota=id_nota, nota=nota)

@router.patch('/update_puntuacion/{id_nota}', response_model=nota_schemas.Nota)
def update_puntuacion_nota(id_nota: int, nota: nota_schemas.NotaPuntuacionUpdate, db: Session = Depends(get_db)):
    db_nota = nota_crud.get_nota_por_id(db, id_nota=id_nota)
    if db_nota is None:
        raise HTTPException(status_code=404, detail='Nota no encontrada')
    return nota_crud.update_puntuacion_nota(db=db, id_nota=id_nota, nota=nota)

@router.put('/update_status/{id_nota}', response_model=nota_schemas.Nota)
def update_estatus_nota(id_nota: int, nota: nota_schemas.NotaEstatusUpdate, db: Session = Depends(get_db)):
    db_nota = nota_crud.get_nota_por_id(db, id_nota=id_nota)
    if db_nota is None:
        raise HTTPException(status_code=404, detail='Nota no encontrada')
    return nota_crud.update_estatus_nota(db=db, id_nota=id_nota, nota=nota)

# Eliminar una nota registrada, por ID

@router.delete('/delete/{id_nota}', response_model=nota_schemas.Nota)
def delete_nota(id_nota: int, db: Session = Depends(get_db)):
    db_nota = nota_crud.get_nota_por_id(db, id_nota=id_nota)
    if db_nota is None:
        raise HTTPException(status_code=404, detail='Nota no encontrada')
    return nota_crud.delete_nota(db=db, id_nota=id_nota)