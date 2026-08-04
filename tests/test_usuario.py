from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_criar_usuario():
    resposta = client.post("/usuario/",
    json={
        "nome": "Teste",
        "email": "test@email.com",
        "senha": "senha123"
    })

    assert resposta.status_code == 200
    assert resposta.json()["email"] == "test@email.com"

def test_login():
    resposta = client.post("/login/",
    data={
        "username": "test@email.com",
        "password": "senha123"
    })

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()