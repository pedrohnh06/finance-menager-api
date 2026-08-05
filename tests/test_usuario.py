import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_criar_usuario():
    uid = str(uuid.uuid4())[:8]
    email = f"test.{uid}@email.com"
    resposta = client.post("/usuario/",
    json={
        "nome": "Teste",
        "email": email,
        "senha": "senha123"
    })

    assert resposta.status_code == 200
    assert resposta.json()["email"] == email

def test_login():
    resposta = client.post("/login/",
    data={
        "username": "test@email.com",
        "password": "senha123"
    })

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()