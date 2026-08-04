# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import  relationship
from src.database import Base
from datetime import datetime


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, unique=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    descricao = Column(String)

    valor = Column(Float)

    tipo = Column(String)

    categoria = relationship("Categoria")

    data = Column(DateTime, default=datetime.now)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)