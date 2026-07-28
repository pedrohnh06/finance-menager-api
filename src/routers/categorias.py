from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from src import models, schemas
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.CategoriaResponse)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    nova_categoria = models.Categoria(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria

@router.get("/", response_model=list[schemas.CategoriaResponse])
def mostrar_categorias(db: Session = Depends(get_db)):
    result = db.query(models.Categoria).all()

    return result