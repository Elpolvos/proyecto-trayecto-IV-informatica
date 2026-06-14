from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_asignatura as asignatura_crud
from backend.src.schemas import schemas_asignatura as asignatura_schemas

router = APIRouter()

# Obtener asignaturas, sea todos, por ID, por usuario-docente o por seccion.

@router.get('/', response_model=List[asignatura_schemas.Asignatura])
def read_asignaturas(db: Session = Depends(get_db)):
    return asignatura_crud.get_asignaturas(db)

@router.get('/{id_asignatura}', response_model=asignatura_schemas.Asignatura)
def read_asignatura_por_id(id_asignatura: int, db: Session = Depends(get_db)):
    db_asignatura = asignatura_crud.get_asignatura_por_id(db, id_asignatura=id_asignatura)
    if db_asignatura is None:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    return db_asignatura

@router.get('/docente/{fk_usuario_id}', response_model=List[asignatura_schemas.Asignatura])
def read_asignaturas_por_docente(fk_usuario_id: int, db: Session = Depends(get_db)):
    return asignatura_crud.get_asignaturas_por_docente(db, fk_usuario_id=fk_usuario_id)

@router.get('/seccion/{fk_seccion_id}', response_model=List[asignatura_schemas.Asignatura])
def read_asignaturas_por_seccion(fk_seccion_id: int, db: Session = Depends(get_db)):
    return asignatura_crud.get_asignaturas_por_seccion(db, fk_seccion_id=fk_seccion_id)

# Registrar una asignatura nueva

@router.post('/create', response_model=asignatura_schemas.Asignatura)
def create_asignatura(asignatura: asignatura_schemas.AsignaturaCreate, db: Session = Depends(get_db)):
    return asignatura_crud.create_asignatura(db=db, asignatura=asignatura)

# Actualizar una asignatura registrada, por ID. Y actualizar tambien el estatus de la asignatura (Soft-Delete)

@router.put('/update/{id_asignatura}', response_model=asignatura_schemas.Asignatura)
def update_asignatura(id_asignatura: int, asignatura: asignatura_schemas.AsignaturaCreate, db: Session = Depends(get_db)):
    db_asignatura = asignatura_crud.get_asignatura_por_id(db, id_asignatura=id_asignatura)
    if db_asignatura is None:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    return asignatura_crud.update_asignatura(db=db, id_asignatura=id_asignatura, asignatura=asignatura)

@router.put('/update_status/{id_asignatura}', response_model=asignatura_schemas.Asignatura)
def update_estatus_asignatura(id_asignatura: int, asignatura: asignatura_schemas.AsignaturaEstatusUpdate, db: Session = Depends(get_db)):
    db_asignatura = asignatura_crud.get_asignatura_por_id(db, id_asignatura=id_asignatura)
    if db_asignatura is None:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    return asignatura_crud.update_estatus_asignatura(db=db, id_asignatura=id_asignatura, asignatura=asignatura)

# Eliminar una asignatura registrada, por ID

@router.delete('/delete/{id_asignatura}', response_model=asignatura_schemas.Asignatura)
def delete_asignatura(id_asignatura: int, db: Session = Depends(get_db)):
    db_asignatura = asignatura_crud.get_asignatura_por_id(db, id_asignatura=id_asignatura)
    if db_asignatura is None:
        raise HTTPException(status_code=404, detail='Asignatura no encontrada')
    return asignatura_crud.delete_asignatura(db=db, id_asignatura=id_asignatura)