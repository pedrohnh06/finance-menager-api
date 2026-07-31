from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Categoria

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
    data: Optional[datetime] = None

# Transacao

class TransacaoResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str
    categoria_id: int
    data: datetime

    class Config:
        from_attributes = True

class TransacaoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    tipo: Optional[str] = None
    categoria_id: Optional[int] = None
    data: Optional[datetime] = None

# Usuario

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True

# Senha

class Token(BaseModel):
    access_token: str
    token_type: str
    