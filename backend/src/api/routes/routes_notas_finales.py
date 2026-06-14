from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.src.api.deps import get_db
from backend.src.crud import crud_notas_finales as nota_final_crud
from backend.src.schemas import schemas_notas_finales as nota_final_schemas

router = APIRouter()

# Obtener notas finales, sea todos, por ID, por usuario-estudiante, por asignatura o por trimestre

@router.get('/', response_model=List[nota_final_schemas.NotaFinal])
def read_notas_finales(db: Session = Depends(get_db)):
    return nota_final_crud.get_notas_finales(db)

@router.get('/{id_nota_final}', response_model=nota_final_schemas.NotaFinal)
def read_nota_final_por_id(id_nota_final: int, db: Session = Depends(get_db)):
    db_nota_final = nota_final_crud.get_nota_final_por_id(db, id_nota_final=id_nota_final)
    if db_nota_final is None:
        raise HTTPException(status_code=404, detail='Nota final no encontrada')
    return db_nota_final

@router.get('/estudiante/{fk_usuario_id}', response_model=List[nota_final_schemas.NotaFinal])
def read_notas_finales_por_estudiante(fk_usuario_id: int, db: Session = Depends(get_db)):
    return nota_final_crud.get_notas_finales_por_estudiante(db, fk_usuario_id=fk_usuario_id)

@router.get('/asignatura/{fk_asignatura_id}', response_model=List[nota_final_schemas.NotaFinal])
def read_notas_finales_por_asignatura(fk_asignatura_id: int, db: Session = Depends(get_db)):
    return nota_final_crud.get_notas_finales_por_asignatura(db, fk_asignatura_id=fk_asignatura_id)

@router.get('/trimestre/{fk_trimestre_id}', response_model=List[nota_final_schemas.NotaFinal])
def read_notas_finales_por_trimestre(fk_trimestre_id: int, db: Session = Depends(get_db)):
    return nota_final_crud.get_notas_finales_por_trimestre(db, fk_trimestre_id=fk_trimestre_id)

# Registrar una nota final nueva

@router.post('/create', response_model=nota_final_schemas.NotaFinal)
def create_nota_final(nota_final: nota_final_schemas.NotaFinalCreate, db: Session = Depends(get_db)):
    db_nota_final = nota_final_crud.get_nota_final_por_estudiante_asignatura_trimestre(db, fk_usuario_id=nota_final.fk_usuario_id, fk_asignatura_id=nota_final.fk_asignatura_id, fk_trimestre_id=nota_final.fk_trimestre_id)
    if db_nota_final:
        raise HTTPException(status_code=400, detail='La nota final para este estudiante, asignatura y trimestre ya existe')
    return nota_final_crud.create_nota_final(db=db, nota_final=nota_final)

# Actualizar una nota final registrada, por ID. Además, actualizar la puntuación del promedio de la nota final, tambien por ID. Y actualizar tambien el estatus de la nota (Soft-Delete)

@router.put('/update/{id_nota_final}', response_model=nota_final_schemas.NotaFinal)
def update_nota_final(id_nota_final: int, nota_final: nota_final_schemas.NotaFinalCreate, db: Session = Depends(get_db)):
    db_nota_final = nota_final_crud.get_nota_final_por_id(db, id_nota_final=id_nota_final)
    if db_nota_final is None:
        raise HTTPException(status_code=404, detail='Nota final no encontrada')
    return nota_final_crud.update_nota_final(db=db, id_nota_final=id_nota_final, nota_final=nota_final)

@router.patch('/update_promedio/{id_nota_final}', response_model=nota_final_schemas.NotaFinal)
def update_promedio_nota_final(id_nota_final: int, nota_final: nota_final_schemas.NotaFinalPromedioUpdate, db: Session = Depends(get_db)):
    db_nota_final = nota_final_crud.get_nota_final_por_id(db, id_nota_final=id_nota_final)
    if db_nota_final is None:
        raise HTTPException(status_code=404, detail='Nota final no encontrada')
    return nota_final_crud.update_promedio_nota_final(db=db, id_nota_final=id_nota_final, nota_final=nota_final)

@router.put('/update_status/{id_nota_final}', response_model=nota_final_schemas.NotaFinal)
def update_estatus_nota_final(id_nota_final: int, nota_final: nota_final_schemas.NotaFinalEstatusUpdate, db: Session = Depends(get_db)):
    db_nota_final = nota_final_crud.get_nota_final_por_id(db, id_nota_final=id_nota_final)
    if db_nota_final is None:
        raise HTTPException(status_code=404, detail='Nota final no encontrada')
    return nota_final_crud.update_estatus_nota_final(db=db, id_nota_final=id_nota_final, nota_final=nota_final)

# Eliminar una nota final registrada, por ID

@router.delete('/delete/{id_nota_final}', response_model=nota_final_schemas.NotaFinal)
def delete_nota_final(id_nota_final: int, db: Session = Depends(get_db)):
    db_nota_final = nota_final_crud.get_nota_final_por_id(db, id_nota_final=id_nota_final)
    if db_nota_final is None:
        raise HTTPException(status_code=404, detail='Nota final no encontrada')
    return nota_final_crud.delete_nota_final(db=db, id_nota_final=id_nota_final)