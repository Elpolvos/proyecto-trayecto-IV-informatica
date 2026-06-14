from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.core.config import settings
from backend.src.api.middleware.logging_middleware import LoggingMiddleware
from backend.src.core.logging import logger

from backend.src.api.routes import auth

from backend.src.api.routes import routes_usuario
from backend.src.api.routes import routes_rol

#from backend.src.api.routes import routes_administrador
#from backend.src.api.routes import routes_docente
#from backend.src.api.routes import routes_estudiante

from backend.src.api.routes import routes_seccion
from backend.src.api.routes import routes_trimestre
from backend.src.api.routes import routes_asignatura
from backend.src.api.routes import routes_evaluacion
#from backend.src.api.routes import routes_notas
from backend.src.api.routes import routes_notas_finales
from backend.src.api.routes import routes_asistencia
from backend.src.api.routes import routes_inscripcion

from backend.src.api.routes import routes_aprobacion



app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')

def index():
    return {"Msg" : "Hola mundo uwu"}

# Agregar middleware
app.add_middleware(LoggingMiddleware)

# Log de inicio
@app.on_event("startup")
async def startup_event():
    logger.info("=== API del Colegio iniciada correctamente ===")
    logger.info("Todos los módulos cargados y listos para usar")

app.include_router(auth.router, prefix='/api/v1')

# PERSONAL

app.include_router(routes_usuario.router, prefix='/api/v1/usuarios', tags=['Usuarios'])
app.include_router(routes_rol.router, prefix='/api/v1/roles', tags=['Roles'])

#app.include_router(routes_administrador.router, prefix='/administradores', tags=['Administradores'])
#app.include_router(routes_docente.router, prefix='/docentes', tags=['Docentes'])
#app.include_router(routes_estudiante.router, prefix='/estudiantes', tags=['Estudiantes'])

# SEGUIMIENTO

app.include_router(routes_seccion.router, prefix='/api/v1/secciones', tags=['Secciones'])
app.include_router(routes_trimestre.router, prefix='/api/v1/trimestres', tags=['Trimestres'])
app.include_router(routes_asignatura.router, prefix='/api/v1/asignaturas', tags=['Asignaturas'])
app.include_router(routes_evaluacion.router, prefix='/api/v1/evaluaciones', tags=['Evaluaciones'])

#app.include_router(routes_notas.router, prefix='/notas', tags=['Notas'])

app.include_router(routes_notas_finales.router, prefix='/api/v1/notas_finales', tags=['Notas Finales'])
app.include_router(routes_aprobacion.router, prefix='/api/v1/estados_aprobaciones', tags=['Estados de Aprobacion'])
app.include_router(routes_asistencia.router, prefix='/api/v1/asistencias', tags=['Asistencias'])
app.include_router(routes_inscripcion.router, prefix='/api/v1/inscripciones', tags=['Inscripciones'])

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("=== API del Colegio cerrada ===")