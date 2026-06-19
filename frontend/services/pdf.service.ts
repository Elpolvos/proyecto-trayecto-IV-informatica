import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import { Platform } from 'react-native';

interface BoletínData {
  estudiante: {
    nombre: string;
    apellido: string;
    dni: string;
    seccion: string;
  };
  trimestre: {
    nombre: string;
    periodo: string;
  };
  materias: Array<{
    nombre: string;
    evaluacion1: number | null;
    evaluacion2: number | null;
    evaluacion3: number | null;
    promedio: number;
    estatus: 'aprobado' | 'reprobado';
  }>;
  promedioGeneral: number;
  asistencia: {
    porcentaje: number;
    totalDias: number;
    asistencias: number;
    faltas: number;
  };
  fechaEmision: string;
}

export const pdfService = {
  generateDocentesMateriasHTML: (docentes: any[]): string => {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Listado de Docentes y Materias</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          h1 { color: #1565c0; text-align: center; }
          table { width: 100%; border-collapse: collapse; margin-top: 20px; }
          th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
          th { background-color: #f2f2f2; color: #1565c0; }
        </style>
      </head>
      <body>
        <h1>Listado de Docentes y Materias</h1>
        <table>
          <thead>
            <tr>
              <th>Docente</th>
              <th>DNI</th>
              <th>Materia(s) Asignada(s)</th>
            </tr>
          </thead>
          <tbody>
            ${docentes.map(d => `
              <tr>
                <td>${d.nombre} ${d.apellido}</td>
                <td>${d.dni}</td>
                <td>${d.materias || 'Sin asignar'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </body>
      </html>
    `;
  },

  generateEstudiantesSeccionHTML: (estudiantes: any[], seccion: string): string => {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Estudiantes - Sección ${seccion}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          h1 { color: #1565c0; text-align: center; }
          table { width: 100%; border-collapse: collapse; margin-top: 20px; }
          th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
          th { background-color: #f2f2f2; color: #1565c0; }
        </style>
      </head>
      <body>
        <h1>Listado de Estudiantes - Sección ${seccion}</h1>
        <table>
          <thead>
            <tr>
              <th>Nombre Completo</th>
              <th>DNI</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            ${estudiantes.map(e => `
              <tr>
                <td>${e.apellido}, ${e.nombre}</td>
                <td>${e.dni}</td>
                <td>${e.email}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </body>
      </html>
    `;
  },

  generateBoletinHTML: (data: BoletínData): string => {
    const getEstatusColor = (estatus: string) => {
      return estatus === 'aprobado' ? '#4caf50' : '#f44336';
    };

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Boletín de Calificaciones</title>
        <style>
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            background-color: #f5f5f5;
            padding: 40px;
          }
          .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
          }
          .header {
            background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
            color: white;
            padding: 30px;
            text-align: center;
          }
          .header h1 {
            font-size: 28px;
            margin-bottom: 8px;
          }
          .header p {
            font-size: 14px;
            opacity: 0.9;
          }
          .info-section {
            padding: 24px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
          }
          .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
          }
          .info-item {
            display: flex;
            flex-direction: column;
          }
          .info-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
          }
          .info-value {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-top: 4px;
          }
          .table-section {
            padding: 24px;
          }
          .table-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 16px;
            color: #1565c0;
          }
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th {
            background-color: #e3f2fd;
            padding: 12px;
            text-align: center;
            font-size: 13px;
            font-weight: bold;
            color: #1565c0;
            border: 1px solid #ddd;
          }
          td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
            font-size: 14px;
          }
          .materia-nombre {
            text-align: left;
            font-weight: 500;
          }
          .aprobado {
            background-color: #e8f5e9;
            color: #2e7d32;
            font-weight: bold;
          }
          .reprobado {
            background-color: #ffebee;
            color: #c62828;
            font-weight: bold;
          }
          .promedio-general {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            padding: 20px;
            margin: 0 24px 24px 24px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }
          .promedio-label {
            font-size: 16px;
            font-weight: bold;
            color: #2e7d32;
          }
          .promedio-value {
            font-size: 32px;
            font-weight: bold;
            color: #1b5e20;
          }
          .asistencia-section {
            padding: 24px;
            background: #f5f5f5;
            border-top: 1px solid #e0e0e0;
          }
          .asistencia-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 16px;
            color: #1565c0;
          }
          .asistencia-stats {
            display: flex;
            justify-content: space-around;
            text-align: center;
          }
          .stat {
            flex: 1;
          }
          .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #1565c0;
          }
          .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 4px;
          }
          .footer {
            background: #fafafa;
            padding: 16px;
            text-align: center;
            font-size: 11px;
            color: #999;
            border-top: 1px solid #e0e0e0;
          }
          @media print {
            body {
              padding: 0;
            }
            .container {
              box-shadow: none;
            }
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>📘 BOLETÍN DE CALIFICACIONES</h1>
            <p>Año Escolar ${new Date().getFullYear()}</p>
          </div>

          <div class="info-section">
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">ESTUDIANTE</span>
                <span class="info-value">${data.estudiante.apellido} ${data.estudiante.nombre}</span>
              </div>
              <div class="info-item">
                <span class="info-label">DNI</span>
                <span class="info-value">${data.estudiante.dni}</span>
              </div>
              <div class="info-item">
                <span class="info-label">SECCIÓN</span>
                <span class="info-value">${data.estudiante.seccion}</span>
              </div>
              <div class="info-item">
                <span class="info-label">TRIMESTRE</span>
                <span class="info-value">${data.trimestre.nombre}</span>
              </div>
              <div class="info-item">
                <span class="info-label">PERÍODO</span>
                <span class="info-value">${data.trimestre.periodo}</span>
              </div>
              <div class="info-item">
                <span class="info-label">FECHA DE EMISIÓN</span>
                <span class="info-value">${data.fechaEmision}</span>
              </div>
            </div>
          </div>

          <div class="table-section">
            <div class="table-title">📊 DETALLE DE CALIFICACIONES</div>
            <table>
              <thead>
                <tr>
                  <th>MATERIA</th>
                  <th>EVAL. 1</th>
                  <th>EVAL. 2</th>
                  <th>EVAL. 3</th>
                  <th>PROMEDIO</th>
                  <th>ESTATUS</th>
                </tr>
              </thead>
              <tbody>
                ${data.materias.map(materia => `
                  <tr>
                    <td class="materia-nombre">${materia.nombre}</td>
                    <td>${materia.evaluacion1 !== null ? materia.evaluacion1 : '-'}</td>
                    <td>${materia.evaluacion2 !== null ? materia.evaluacion2 : '-'}</td>
                    <td>${materia.evaluacion3 !== null ? materia.evaluacion3 : '-'}</td>
                    <td class="${materia.estatus === 'aprobado' ? 'aprobado' : 'reprobado'}">${materia.promedio.toFixed(2)}</td>
                    <td class="${materia.estatus === 'aprobado' ? 'aprobado' : 'reprobado'}">
                      ${materia.estatus === 'aprobado' ? '✓ APROBADO' : '✗ REPROBADO'}
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>

          <div class="promedio-general">
            <span class="promedio-label">📈 PROMEDIO GENERAL DEL TRIMESTRE</span>
            <span class="promedio-value">${data.promedioGeneral.toFixed(2)}</span>
          </div>

          <div class="asistencia-section">
            <div class="asistencia-title">📅 REPORTE DE ASISTENCIA</div>
            <div class="asistencia-stats">
              <div class="stat">
                <div class="stat-value">${data.asistencia.porcentaje}%</div>
                <div class="stat-label">PORCENTAJE</div>
              </div>
              <div class="stat">
                <div class="stat-value">${data.asistencia.asistencias}</div>
                <div class="stat-label">ASISTENCIAS</div>
              </div>
              <div class="stat">
                <div class="stat-value">${data.asistencia.faltas}</div>
                <div class="stat-label">FALTAS</div>
              </div>
              <div class="stat">
                <div class="stat-value">${data.asistencia.totalDias}</div>
                <div class="stat-label">TOTAL DÍAS</div>
              </div>
            </div>
          </div>

          <div class="footer">
            <p>Este documento es una representación oficial de las calificaciones del estudiante.</p>
            <p>Sistema de Gestión Escolar - ${new Date().getFullYear()}</p>
          </div>
        </div>
      </body>
      </html>
    `;
  },

  generateAndSharePDF: async (data: BoletínData): Promise<boolean> => {
    try {
      const html = pdfService.generateBoletinHTML(data);
      return await pdfService.shareHTMLasPDF(html, `Boletin_${data.estudiante.dni}.pdf`);
    } catch (error) {
      console.error('Error generando PDF:', error);
      return false;
    }
  },

  shareHTMLasPDF: async (html: string, fileName: string): Promise<boolean> => {
    try {
      const filePath = `${FileSystem.documentDirectory}${fileName}`;

      if (Platform.OS === 'web') {
        // Para web
        const blob = new Blob([html], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        link.click();
        URL.revokeObjectURL(url);
        return true;
      } else {
        // Para móvil, necesitamos una librería que convierta HTML a PDF
        // Usaremos react-native-html-to-pdf o similar
        // Por ahora, guardamos el HTML y mostramos cómo compartirlo
        await FileSystem.writeAsStringAsync(filePath, html, { encoding: FileSystem.EncodingType.UTF8 });
        
        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(filePath, {
            mimeType: 'text/html',
            dialogTitle: 'Compartir Boletín',
            UTI: 'public.html'
          });
        }
        return true;
      }
    } catch (error) {
      console.error('Error generando PDF:', error);
      return false;
    }
  }
};