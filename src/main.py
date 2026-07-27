from fastapi import FastAPI, Depends
from src import models, database, schemas 
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session


app = FastAPI()

@app.get("/")
def raiz():
    return {"mensagem": "Bem vindo ao Gerenciador Financeiro"}

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/categorias", response_model=schemas.CategoriaResponse)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    nova_categoria = models.Categoria(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria

@app.get("/categorias", response_model=list[schemas.CategoriaResponse])
def mostrar_categorias(db: Session = Depends(get_db)):
    result = db.query(models.Categoria).all()

    return result