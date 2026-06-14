from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_docente as docente_crud
from backend.src.schemas import schemas_docente as docente_schemas

router = APIRouter()

# Obtener docentes, sea todos, por ID o por DNI

@router.get('/', response_model=List[docente_schemas.Docente])
def read_docentes(db: Session = Depends(get_db)):
    return docente_crud.get_docentes(db)

@router.get('/{id_docente}', response_model=docente_schemas.Docente)
def read_docente_por_id(id_docente: int, db: Session = Depends(get_db)):
    db_docente = docente_crud.get_docente_por_id(db, id_docente=id_docente)
    if db_docente is None:
        raise HTTPException(status_code=404, detail='Docente no encontrado')
    return db_docente

@router.get('/dni/{dni_docente}', response_model=docente_schemas.Docente)
def read_docente_por_dni(dni_docente: str, db: Session = Depends(get_db)):
    db_docente = docente_crud.get_docente_por_dni(db, dni_docente=dni_docente)
    if db_docente is None:
        raise HTTPException(status_code=404, detail='Docente no encontrado')
    return db_docente

# Registrar un docente nuevo

@router.post('/create', response_model=docente_schemas.Docente)
def create_docente(docente: docente_schemas.DocenteCreate, db: Session = Depends(get_db)):
    db_docente = docente_crud.get_docente_por_dni(db, dni_docente=docente.dni_docente)
    if db_docente:
        raise HTTPException(status_code=400, detail='Docente ya existente')
    return docente_crud.create_docente(db=db, docente=docente)

# Actualizar un docente registrado, por ID. Y actualizar tambien el estatus del docente (Soft-Delete)

@router.put('/update/{id_docente}', response_model=docente_schemas.Docente)
def update_docente(id_docente: int, docente: docente_schemas.DocenteCreate, db: Session = Depends(get_db)):
    db_docente = docente_crud.get_docente_por_id(db, id_docente=id_docente)
    if db_docente is None:
        raise HTTPException(status_code=404, detail='Docente no encontrado')
    return docente_crud.update_docente(db=db, id_docente=id_docente, docente=docente)

@router.put('/update_status/{id_docente}', response_model=docente_schemas.Docente)
def update_estatus_docente(id_docente: int, docente: docente_schemas.DocenteEstatusUpdate, db: Session = Depends(get_db)):
    db_docente = docente_crud.get_docente_por_id(db, id_docente=id_docente)
    if db_docente is None:
        raise HTTPException(status_code=404, detail='Docente no encontrado')
    return docente_crud.update_estatus_docente(db=db, id_docente=id_docente, docente=docente)

# Eliminar un docente registrado, por ID

@router.delete('/delete/{id_docente}', response_model=docente_schemas.Docente)
def delete_docente(id_docente: int, db: Session = Depends(get_db)):
    db_docente = docente_crud.get_docente_por_id(db, id_docente=id_docente)
    if db_docente is None:
        raise HTTPException(status_code=404, detail='Docente no encontrado')
    return docente_crud.delete_docente(db=db, id_docente=id_docente)