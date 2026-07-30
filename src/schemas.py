from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class TransacaoCreate(BaseModel):
    descricao: str
    valor: float
    tipo: str
    categoria_id: int

class TransacaoResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str
    categoria_id: int

    class Config:
        from_attributes = True

class TransacaoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    tipo: Optional[str] = None
    categoria_id: Optional[int] = None