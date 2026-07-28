from src.routers import categorias, transacoes
from fastapi import FastAPI
from src import models, database
# pyrefly: ignore [missing-import]


app = FastAPI()

@app.get("/")
def raiz():
    return {"mensagem": "Bem vindo ao Gerenciador Financeiro"}

models.Base.metadata.create_all(bind=database.engine)

app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
app.include_router(transacoes.router, prefix="/transacoes", tags=["Transações"])