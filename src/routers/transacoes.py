from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from src import models, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TransacaoResponse)
def criar_transacao(transacao: schemas.TransacaoCreate, db: Session = Depends(get_db)):
    nova_transacao = models.Transacao(descricao=transacao.descricao, valor=transacao.valor, 
    tipo=transacao.tipo, categoria_id=transacao.categoria_id)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)

    return nova_transacao

@router.get("/", response_model=list[schemas.TransacaoResponse])
def mostrar_transacao(db: Session = Depends(get_db)):
    result = db.query(models.Transacao).all()

    return result