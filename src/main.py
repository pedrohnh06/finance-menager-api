from src.routers import categorias, transacoes, usuario, login
from fastapi import FastAPI
from src import models, database

app = FastAPI()

@app.get("/")
def raiz():
    return {"mensagem": "Bem vindo ao Gerenciador Financeiro"}

models.Base.metadata.create_all(bind=database.engine)

app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
app.include_router(transacoes.router, prefix="/transacoes", tags=["Transações"])
app.include_router(usuario.router, prefix="/usuario", tags=["Usuários"])
app.include_router(login.router, prefix="/login", tags=["Login"])