
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String
from src.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, unique=True, index=True)