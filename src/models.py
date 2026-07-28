# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Float, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from src.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, unique=True, index=True)

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    descricao = Column(String)

    valor = Column(Float)

    tipo = Column(String)

    categoria = relationship("Categoria")