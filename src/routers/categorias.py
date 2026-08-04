from src import auth
from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from src import models, schemas
from src.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.CategoriaResponse)
def criar_categoria(categoria: schemas.CategoriaCreate,
 db: Session = Depends(get_db),
 usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    nova_categoria = models.Categoria(
        nome=categoria.nome,
        usuario_id=usuario_logado.id
        )
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria

@router.get("/", response_model=list[schemas.CategoriaResponse])
def mostrar_categorias(db: Session = Depends(get_db),
usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    result = db.query(
        models.Categoria
        ).filter(
        models.Categoria.usuario_id == usuario_logado.id
    ).all()

    return result

@router.delete("/{categoria_id}")
def deletar_categoria(categoria_id: int,
 db: Session = Depends(get_db),
 usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    buscador = db.query(
        models.Categoria
        ).filter(
            models.Categoria.id == categoria_id,
            models.Categoria.usuario_id == usuario_logado.id
            ).first()
    
    if not buscador:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    else:
        db.delete(buscador)
        db.commit()
        return {"mensagem": "Categoria deletada com sucesso!"}

@router.put("/{categoria_id}", response_model=schemas.CategoriaResponse)
def atualizar_categoria(categoria_id: int,
 categoria:schemas.CategoriaCreate,
  db: Session = Depends(get_db),
  usuario_logado: models.Usuario = Depends(auth.obter_usuario_atual)):
    buscador = db.query(
        models.Categoria
        ).filter(
            models.Categoria.id == categoria_id,
            models.Categoria.usuario_id == usuario_logado.id
            ).first()
    if not buscador:
        raise HTTPException(status_code=404, detail="Categoia não encontrada")
    else:
        buscador.nome = categoria.nome
        db.commit()
        db.refresh(buscador)
        return buscador