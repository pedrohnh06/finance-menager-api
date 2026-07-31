# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src import models, schemas, auth
from src.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    senha_criptografada = auth.hash_senha(usuario.senha)

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_criptografada
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario