# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from src import models, schemas, auth
from src.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/", response_model=schemas.Token)
def fazer_login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    buscador = db.query(models.Usuario).filter(models.Usuario.email == login_data.username).first()
    if not buscador:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    else:
        verificar = auth.verificar_senha(login_data.password, buscador.senha_hash)
        if verificar is False:
            raise HTTPException(status_code=401, detail="Email ou senha incorretos")
        else:
            dados_token = {"sub": buscador.email}

            token_gerado = auth.criar_token_acesso(dados_token)

            return {"access_token": token_gerado, "token_type": "bearer"}