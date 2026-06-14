import api from './api';

export interface Evaluacion {
  id_evaluacion: number;
  numero_evaluacion: string;
  descripcion_evaluacion: string;
  porcentaje_evaluacion: number;
}

export interface Nota {
  id_nota?: number;
  fk_evaluacion_id: number;
  fk_estudiante_id: number;
  puntuacion_nota: number;
  fecha_registro: string;
}

export const notasService = {
  // Obtener evaluaciones de una asignatura
  getEvaluacionesByAsignatura: async (asignaturaId: number) => {
    const response = await api.get(`/asignaturas/${asignaturaId}/evaluaciones`);
    return response.data;
  },

  // Obtener estudiantes de una sección
  getEstudiantesBySeccion: async (seccionId: number) => {
    const response = await api.get(`/secciones/${seccionId}/estudiantes`);
    return response.data;
  },

  // Obtener notas de un estudiante por asignatura y trimestre
  getNotasEstudiante: async (estudianteId: number, asignaturaId: number, trimestreId: number) => {
    const response = await api.get(`/notas/estudiante/${estudianteId}/asignatura/${asignaturaId}/trimestre/${trimestreId}`);
    return response.data;
  },

  // Registrar o actualizar una nota
  saveNota: async (notaData: Nota) => {
    if (notaData.id_nota) {
      const response = await api.put(`/notas/${notaData.id_nota}`, notaData);
      return response.data;
    } else {
      const response = await api.post('/notas', notaData);
      return response.data;
    }
  },

  // Registrar múltiples notas a la vez
  saveMultipleNotas: async (notas: Nota[]) => {
    const response = await api.post('/notas/batch', { notas });
    return response.data;
  },

  // Calcular promedio de un estudiante en una asignatura
  calcularPromedio: async (estudianteId: number, asignaturaId: number, trimestreId: number) => {
    const response = await api.get(`/notas/promedio/estudiante/${estudianteId}/asignatura/${asignaturaId}/trimestre/${trimestreId}`);
    return response.data;
  }
};