from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from src import models, schemas
from src.database import get_db

router = APIRouter()


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

@router.delete("/{transacao_id}")
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db)):
    buscador = db.query(models.Transacao).filter(models.Transacao.id == transacao_id).first()

    if not buscador:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    else:
        db.delete(buscador)
        db.commit()
        return {"mensagem": "Transação deletada com sucesso!"}

@router.patch("/{transacao_id}", response_model=schemas.TransacaoResponse)
def atualizar_transacao(transacao_id: int, transacao: schemas.TransacaoUpdate, db: Session = Depends(get_db)):
    buscador = db.query(models.Transacao).filter(models.Transacao.id == transacao_id).first()
    if not buscador:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    else:
        if transacao.descricao is not None:
            buscador.descricao = transacao.descricao
        if transacao.valor is not None:
            buscador.valor = transacao.valor
        if transacao.tipo is not None:
            buscador.tipo = transacao.tipo
        if transacao.categoria_id is not None:
            buscador.categoria_id = transacao.categoria_id
        db.commit()
        db.refresh(buscador)
        return buscador                                     