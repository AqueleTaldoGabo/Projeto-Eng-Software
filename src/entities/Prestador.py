from src.database import Base
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship


class Prestador(Base):
    __tablename__ = "prestadores"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    servicos = relationship("Servico", back_populates="prestador_rel")