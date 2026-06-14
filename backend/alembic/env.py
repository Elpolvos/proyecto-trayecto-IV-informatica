from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

from backend.src.db.base_class import Base

from backend.src.models.models_usuario import Usuarios
from backend.src.models.models_rol import Roles

#from backend.src.models.models_estudiante import Estudiantes
#from backend.src.models.models_docente import Docentes
#from backend.src.models.models_administrador import Administradores

from backend.src.models.models_inscripcion import Inscripciones
from backend.src.models.models_asignatura import Asignaturas
from backend.src.models.models_asistencia import Asistencias
from backend.src.models.models_seccion import Secciones
#from backend.src.models.models_notas import Notas
from backend.src.models.models_evaluacion import Evaluaciones
from backend.src.models.models_notas_finales import Notas_Finales
from backend.src.models.models_trimestre import Trimestres

from backend.src.models.models_aprobacion import Estados_Aprobaciones
from backend.src.models.models_auditoria import Auditoria

load_dotenv()
config = context.config
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
