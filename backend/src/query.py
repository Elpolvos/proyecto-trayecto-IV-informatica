from sqlalchemy import func, and_, extract, case
from sqlalchemy.orm import Session
from datetime import datetime, date

from src.models.models_estudiante import Estudiantes
from src.models.models_docente import Docentes
from src.models.models_administrador import Administradores
from src.models.models_inscripcion import Inscripciones
from src.models.models_asignatura import Asignaturas
from src.models.models_asistencia import Asistencias
from src.models.models_seccion import Secciones
from src.models.models_notas import Notas
from src.models.models_evaluacion import Evaluaciones
from models.models_notas_finales import Notas_Finales
from src.models.models_trimestre import Trimestres

class ReportesAcademico:
    
    def __init__(self, db: Session):
        self.db = db
    
    # ============================================
    # 1. Boletín de notas de un estudiante
    # ============================================
    def boletin_estudiante(self, estudiante_id: int, trimestre_id: int = None):
        """Obtiene todas las notas de un estudiante por trimestre"""
        query = self.db.query(
            Asignaturas.nombre_asignatura,
            Trimestres.nombre_trimestre,
            func.avg(Notas.puntuacion_nota).label('promedio'),
            Notas_Finales.estado_aprobacion,
            Notas_Finales.porcentaje_asistencia
        ).join(
            Notas_Finales, Notas_Finales.fk_asignatura_id == Asignaturas.id_asignatura
        ).join(
            Trimestres, Trimestres.id_trimestre == Notas_Finales.fk_trimestre_id
        ).filter(
            Notas_Finales.fk_estudiante_id == estudiante_id
        )
        
        if trimestre_id:
            query = query.filter(Notas_Finales.fk_trimestre_id == trimestre_id)
        
        return query.group_by(
            Asignaturas.nombre_asignatura, 
            Trimestres.nombre_trimestre,
            Notas_Finales.estado_aprobacion,
            Notas_Finales.porcentaje_asistencia
        ).all()
    
    # ============================================
    # 2. Reporte de asistencia por asignatura
    # ============================================
    def reporte_asistencia(self, asignatura_id: int, fecha_inicio: date, fecha_fin: date):
        """Porcentaje de asistencia por estudiante en una asignatura"""
        total_clases = self.db.query(func.count(Asistencias.fecha_asistencia.distinct()))\
            .filter(
                Asistencias.fk_asignatura_id == asignatura_id,
                Asistencias.fecha_asistencia.between(fecha_inicio, fecha_fin)
            ).scalar()
        
        resultados = self.db.query(
            Estudiantes.id_estudiante,
            Estudiantes.nombre_estudiante,
            Estudiantes.apellido_estudiante,
            func.count(Asistencias.id_asistencia).label('asistencias'),
            func.sum(case((Asistencias.presente == True, 1), else_=0)).label('presente')
        ).join(
            Asistencias, Asistencias.fk_estudiante_id == Estudiantes.id_estudiante
        ).filter(
            Asistencias.fk_asignatura_id == asignatura_id,
            Asistencias.fecha_asistencia.between(fecha_inicio, fecha_fin)
        ).group_by(
            Estudiantes.id_estudiante, Estudiantes.nombre_estudiante, Estudiantes.apellido_estudiante
        ).all()
        
        for r in resultados:
            r.porcentaje = (r.presente / total_clases * 100) if total_clases > 0 else 0
        
        return resultados
    
    # ============================================
    # 3. Promedio general por sección y asignatura
    # ============================================
    def promedio_seccion_asignatura(self, seccion_id: int, trimestre_id: int):
        """Promedio general de una sección por asignatura"""
        return self.db.query(
            Asignaturas.nombre_asignatura,
            func.avg(Notas_Finales.nota_promedio).label('promedio_seccion'),
            func.count(Notas_Finales.fk_estudiante_id.distinct()).label('total_estudiantes')
        ).join(
            Notas_Finales, Notas_Finales.fk_asignatura_id == Asignaturas.id_asignatura
        ).join(
            Inscripciones, Inscripciones.fk_estudiante_id == Notas_Finales.fk_estudiante_id
        ).filter(
            Inscripciones.fk_seccion_id == seccion_id,
            Notas_Finales.fk_trimestre_id == trimestre_id,
            Inscripciones.anio_escolar == str(datetime.now().year)
        ).group_by(
            Asignaturas.nombre_asignatura
        ).all()
    
    # ============================================
    # 4. Top de mejores estudiantes por trimestre
    # ============================================
    def top_estudiantes(self, trimestre_id: int, limit: int = 10):
        """Estudiantes con mejor promedio general"""
        return self.db.query(
            Estudiantes.id_estudiante,
            Estudiantes.nombre_estudiante,
            Estudiantes.apellido_estudiante,
            func.avg(Notas_Finales.nota_promedio).label('promedio_general')
        ).join(
            Notas_Finales, Notas_Finales.fk_estudiante_id == Estudiantes.id_estudiante
        ).filter(
            Notas_Finales.fk_trimestre_id == trimestre_id
        ).group_by(
            Estudiantes.id_estudiante
        ).order_by(
            func.avg(Notas_Finales.nota_promedio).desc()
        ).limit(limit).all()
    
    # ============================================
    # 5. Estudiantes en riesgo (promedio < 60)
    # ============================================
    def estudiantes_riesgo(self, trimestre_id: int):
        """Estudiantes con promedio menor a 60"""
        return self.db.query(
            Estudiantes.id_estudiante,
            Estudiantes.nombre_estudiante,
            Estudiantes.apellido_estudiante,
            Asignaturas.nombre_asignatura,
            Notas_Finales.nota_promedio,
            Notas_Finales.porcentaje_asistencia
        ).join(
            Notas_Finales, Notas_Finales.fk_estudiante_id == Estudiantes.id_estudiante
        ).join(
            Asignaturas, Asignaturas.id_asignatura == Notas_Finales.fk_asignatura_id
        ).filter(
            Notas_Finales.fk_trimestre_id == trimestre_id,
            Notas_Finales.nota_promedio < 60
        ).all()
    
    # ============================================
    # 6. Resumen de aprobados/reprobados por asignatura
    # ============================================
    def resumen_aprobacion(self, trimestre_id: int):
        """Cantidad de aprobados y reprobados por asignatura"""
        return self.db.query(
            Asignaturas.nombre_asignatura,
            func.sum(case((Notas_Finales.estado_aprobacion == 'Aprobado', 1), else_=0)).label('aprobados'),
            func.sum(case((Notas_Finales.estado_aprobacion == 'Reprobado', 1), else_=0)).label('reprobados'),
            func.sum(case((Notas_Finales.estado_aprobacion == 'Aplazado', 1), else_=0)).label('aplazados'),
            func.count(Notas_Finales.id_nota_final).label('total')
        ).join(
            Asignaturas, Asignaturas.id_asignatura == Notas_Finales.fk_asignatura_id
        ).filter(
            Notas_Finales.fk_trimestre_id == trimestre_id
        ).group_by(
            Asignaturas.nombre_asignatura
        ).all()
    
    # ============================================
    # 7. Detalle de notas por evaluación
    # ============================================
    def detalle_notas_evaluacion(self, evaluacion_id: int):
        """Lista de estudiantes con sus notas en una evaluación específica"""
        return self.db.query(
            Estudiantes.id_estudiante,
            Estudiantes.nombre_estudiante,
            Estudiantes.apellido_estudiante,
            Notas.puntuacion_nota,
            Evaluaciones.descripcion_evaluacion,
            Evaluaciones.porcentaje_evaluacion
        ).join(
            Notas, Notas.fk_estudiante_id == Estudiantes.id_estudiante
        ).join(
            Evaluaciones, Evaluaciones.id_evaluacion == Notas.fk_evaluacion_id
        ).filter(
            Evaluaciones.id_evaluacion == evaluacion_id
        ).order_by(
            Notas.puntuacion_nota.desc()
        ).all()
    
    # ============================================
    # 8. Historial académico completo del estudiante
    # ============================================
    def historial_estudiante(self, estudiante_id: int):
        """Todas las notas finales por trimestre y año"""
        return self.db.query(
            Trimestres.nombre_trimestre,
            Asignaturas.nombre_asignatura,
            Notas_Finales.nota_promedio,
            Notas_Finales.estado_aprobacion,
            Notas_Finales.porcentaje_asistencia,
            extract('year', Trimestres.fecha_inicio).label('año')
        ).join(
            Notas_Finales, Notas_Finales.fk_trimestre_id == Trimestres.id_trimestre
        ).join(
            Asignaturas, Asignaturas.id_asignatura == Notas_Finales.fk_asignatura_id
        ).filter(
            Notas_Finales.fk_estudiante_id == estudiante_id
        ).order_by(
            Trimestres.fecha_inicio.desc(),
            Asignaturas.nombre_asignatura
        ).all()