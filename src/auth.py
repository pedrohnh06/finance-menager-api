# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = ""
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_senha(senha: str) -> str:
    """Transforma a senha em texto puro em um hash irreversível"""
    return pwd_context.hash(senha)

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash salvo no banco"""
    return  pwd_context.verify(senha_pura,senha_hash)

def criar_token_acesso(dados: dict):
    to_encode = dados.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token_jwt = jwt.encode(to_encode ,SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt

def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") 

        if email is None:
            raise HTTPException(status_code=401, detail="Pulseira sem nome(Token inválido)")

        return email 

    except JWTError:
        raise HTTPException(status_code=401, detail="Pulseira falsa ou vencida")