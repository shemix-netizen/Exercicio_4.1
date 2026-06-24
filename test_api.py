"""
Teste de fumaça (smoke test) da API do Exercício 4.1.

Sobe a API em memória com o TestClient do FastAPI e valida o contrato:
health, POST, GET (item e lista), PUT e o 404.

Como rodar:
    pip install -r requirements.txt
    pytest -v
ou simplesmente:
    python test_api.py
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_post_cria_id_1_concluida_false():
    r = client.post("/tarefas", json={"titulo": "estudar APIs"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "titulo": "estudar APIs", "concluida": False}


def test_get_item_e_lista():
    r = client.get("/tarefas/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1

    r = client.get("/tarefas")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_put_atualiza():
    r = client.put(
        "/tarefas/1",
        json={"titulo": "estudar APIs REST", "concluida": True},
    )
    assert r.status_code == 200
    assert r.json() == {"id": 1, "titulo": "estudar APIs REST", "concluida": True}


def test_404_inexistente():
    assert client.get("/tarefas/99").status_code == 404
    assert client.put(
        "/tarefas/99", json={"titulo": "x", "concluida": False}
    ).status_code == 404


if __name__ == "__main__":
    test_health()
    test_post_cria_id_1_concluida_false()
    test_get_item_e_lista()
    test_put_atualiza()
    test_404_inexistente()
    print("Todos os testes passaram com sucesso.")
