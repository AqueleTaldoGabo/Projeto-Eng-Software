from src.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Float, ForeignKey
from sqlalchemy.orm import relationship

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    descricao = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    tempo_estimado = Column(String, nullable=False)
    status = Column(String, nullable=False)
    
    avaliacao = Column(Float, nullable=True, default=0.0)
    quantavaliacao = Column(Integer, nullable=False, default=0)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    prestador_id = Column(Integer, ForeignKey("prestadores.id"), nullable=False)
    prestador_rel = relationship("Prestador", back_populates="servicos")