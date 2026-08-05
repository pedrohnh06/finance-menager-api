import uuid
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_filtros_mes_ano():
    uid = str(uuid.uuid4())[:8]
    
    client.post("/usuario/",
     json={"nome": "Teste Mes", "email": f"teste.{uid}@email.com", "senha": "123"})

    login_response = client.post("/login/", data={
        "username": f"teste.{uid}@email.com",
        "password": "123"
     })
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    cat_res = client.post("/categorias/", json={"nome": f"Salário {uid}"}, headers=headers)
    cat_id = cat_res.json()["id"]

    client.post("/transacoes/", json={
        "descricao": "Pagamento Julho",
        "valor": 1000.0,
        "tipo": "receita",
        "categoria_id": cat_id,
        "data": "2026-07-15T10:00:00"
    }, headers=headers)

    client.post("/transacoes/", json={
        "descricao": "Pagamento Agosto",
        "valor": 1500.0,
        "tipo": "receita",
        "categoria_id": cat_id,
        "data": "2026-08-15T10:00:00"
    }, headers=headers)

    resumo = client.get("/transacoes/resumo?mes=8&ano=2026", headers=headers)
    
    assert resumo.json()["total_receitas"] == 1500.0