# pyrefly: ignore [missing-import]
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str) -> str:
    """Transforma a senha em texto puro em um hash irreversível"""
    return pwd_context.hash(senha)

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash salvo no banco"""
    return  pwd_context.verify(senha_pura,senha_hash)