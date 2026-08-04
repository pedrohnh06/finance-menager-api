from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from sqlalchemy import func
from src import models, schemas
from src.database import get_db
from typing import Optional
from src import auth

router = APIRouter()


@router.post("/", response_model=schemas.TransacaoResponse)
def criar_transacao(transacao: schemas.TransacaoCreate,
 db: Session = Depends(get_db),
 usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):

    nova_transacao = models.Transacao(descricao=transacao.descricao,
    valor=transacao.valor, 
    tipo=transacao.tipo,
    categoria_id=transacao.categoria_id,
    usuario_id=usuario_logado.id)

    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)

    return nova_transacao

@router.get("/", response_model=list[schemas.TransacaoResponse])
def mostrar_transacao(tipo: Optional[str] = None,
 categoria_id: Optional[int] = None,
 db: Session = Depends(get_db),
 usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    query = db.query(models.Transacao).filter(models.Transacao.usuario_id == usuario_logado.id)


    if tipo is not None:
        query = query.filter(models.Transacao.tipo == tipo)
    if categoria_id is not None:
        query = query.filter(models.Transacao.categoria_id == categoria_id)

    return query.all()

@router.get("/resumo")
def resumo_financeiro(db: Session = Depends(get_db),
usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):

    soma_despesas = (
        db.query(func.sum(models.Transacao.valor))
        .filter(
            models.Transacao.usuario_id == usuario_logado.id,
            models.Transacao.tipo == "despesa"
            ).scalar() or 0
    )

    soma_receitas = (
        db.query(func.sum(models.Transacao.valor))
        .filter(
        models.Transacao.usuario_id == usuario_logado.id,
        models.Transacao.tipo == "receita"
        ).scalar() or 0
        
    )

    saldo_total = soma_receitas - soma_despesas

    return {
        "total_receitas": soma_receitas,
        "total_despesas": soma_despesas,
        "saldo_total": saldo_total
    }

@router.delete("/{transacao_id}")
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db),
 usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    buscador = db.query(
        models.Transacao
        ).filter(
            models.Transacao.id == transacao_id,
            models.Transacao.usuario_id == usuario_logado.id
            ).first()

    if not buscador:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    else:
        db.delete(buscador)
        db.commit()
        return {"mensagem": "Transação deletada com sucesso!"}

@router.patch("/{transacao_id}", response_model=schemas.TransacaoResponse)
def atualizar_transacao(transacao_id: int,
 transacao: schemas.TransacaoUpdate,
  db: Session = Depends(get_db),
  usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    buscador = db.query(
        models.Transacao
        ).filter(
            models.Transacao.id == transacao_id,
            models.Transacao.usuario_id == usuario_logado.id
            ).first()
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
