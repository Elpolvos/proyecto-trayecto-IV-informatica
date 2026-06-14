# backend/api/routes/notas_boletin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.src.api.deps import get_db
from backend.src.models.models_estudiante import Estudiantes
from backend.src.models.models_asignatura import Asignaturas
from backend.src.models.models_notas import Notas
from backend.src.models.models_evaluacion import Evaluaciones
from backend.src.models.models_trimestre import Trimestres
from backend.src.models.models_inscripcion import Inscripciones

router = APIRouter(prefix="/estudiantes", tags=["boletin"])

@router.get("/{estudiante_id}/notas-boletin")
async def get_notas_boletin(
    estudiante_id: int,
    id_trimestre: int,
    db: Session = Depends(get_db)
):
    """Obtiene las notas del estudiante agrupadas por materia para el boletín"""
    
    # Verificar que el estudiante existe
    estudiante = db.query(Estudiantes).filter(Estudiantes.id_estudiante == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Obtener inscripciones del estudiante (las materias que cursa)
    inscripciones = db.query(Inscripciones).filter(
        Inscripciones.fk_estudiante_id == estudiante_id
    ).all()
    
    materias_notas = []
    
    for inscripcion in inscripciones:
        # Obtener la asignatura
        asignatura = db.query(Asignaturas).filter(
            Asignaturas.id_asignatura == inscripcion.fk_asignatura_id
        ).first()
        
        if not asignatura:
            continue
        
        # Obtener evaluaciones de la asignatura para el trimestre
        evaluaciones = db.query(Evaluaciones).filter(
            Evaluaciones.fk_asignatura_id == asignatura.id_asignatura,
            Evaluaciones.fk_trimestre_id == id_trimestre
        ).all()
        
        # Inicializar diccionario de notas
        notas_dict = {}
        for eval in evaluaciones:
            # Buscar la nota del estudiante
            nota = db.query(Notas).filter(
                Notas.fk_evaluacion_id == eval.id_evaluacion,
                Notas.fk_estudiante_id == estudiante_id
            ).first()
            notas_dict[eval.numero_evaluacion] = nota.puntuacion_nota if nota else None
        
        # Calcular promedio
        suma_ponderada = 0
        peso_total = 0
        for eval in evaluaciones:
            nota = notas_dict.get(eval.numero_evaluacion)
            if nota is not None:
                suma_ponderada += nota * (eval.porcentaje_evaluacion / 100)
                peso_total += eval.porcentaje_evaluacion
        
        promedio = suma_ponderada if peso_total > 0 else 0
        
        materias_notas.append({
            "id_asignatura": asignatura.id_asignatura,
            "nombre_asignatura": asignatura.nombre_asignatura,
            "evaluacion1": notas_dict.get("1"),
            "evaluacion2": notas_dict.get("2"),
            "evaluacion3": notas_dict.get("3"),
            "promedio": round(promedio, 2)
        })
    
    return {
        "materias": materias_notas,
        "estudiante": {
            "nombre": estudiante.nombre_estudiante,
            "apellido": estudiante.apellido_estudiante,
            "dni": estudiante.dni_estudiante
        }
    }

@router.get("/{estudiante_id}/asistencia")
async def get_asistencia_estudiante(
    estudiante_id: int,
    id_trimestre: int,
    db: Session = Depends(get_db)
):
    """Obtiene estadísticas de asistencia del estudiante"""
    # Esta es una implementación de ejemplo - ajusta según tu modelo de asistencias
    
    # Asumiendo que tienes una tabla de asistencias
    # Por ahora, devolvemos datos de ejemplo
    return {
        "porcentaje": 92,
        "totalDias": 45,
        "asistencias": 41,
        "faltas": 4
    }