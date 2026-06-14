from sqlalchemy import Column, Integer, Float, String, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from backend.src.db.base_class import Base

class Notas_Finales(Base):
    id_nota_final = Column(Integer, primary_key=True, index=True)
    fk_usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fk_asignatura_id = Column(Integer, ForeignKey("asignaturas.id_asignatura"), nullable=False)
    fk_trimestre_id = Column(Integer, ForeignKey("trimestres.id_trimestre"), nullable=False)
    nota_promedio = Column(Float, nullable=False)  # 0-100
    porcentaje_asistencia = Column(Float, nullable=False)  # 0-100
    fk_estado_aprobacion_id = Column(Integer, ForeignKey("estados_aprobaciones.id_estado_aprobacion"), nullable=False)  # Aprobado, Reprobado, Aplazado
    estatus_nota_final = Column(Boolean, default=True, server_default="true")
    
    # Relationships
    usuario = relationship("Usuarios", back_populates="nota_final")
    asignatura = relationship("Asignaturas", back_populates="nota_final")
    trimestre = relationship("Trimestres", back_populates="nota_final")
    aprobacion = relationship('Estados_Aprobaciones', back_populates='nota_final')
    
    __table_args__ = (
        UniqueConstraint('fk_usuario_id', 'fk_asignatura_id', 'fk_trimestre_id',
                        name='unique_nota_final'),
    )