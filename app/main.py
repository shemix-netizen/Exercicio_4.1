from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Store em memória. Zera quando o processo reinicia.
_tarefas: dict[int, dict] = {}
_proximo_id = 1


class TarefaIn(BaseModel):
    titulo: str


class TarefaUpdate(BaseModel):
    titulo: str
    concluida: bool


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tarefas", status_code=201)
def criar(tarefa: TarefaIn):
    global _proximo_id
    nova = {"id": _proximo_id, "titulo": tarefa.titulo, "concluida": False}
    _tarefas[_proximo_id] = nova
    _proximo_id += 1
    return nova


@app.get("/tarefas")
def listar():
    """Retorna todas as tarefas."""
    return list(_tarefas.values())


@app.get("/tarefas/{id}")
def obter(id: int):
    """Retorna a tarefa com o id informado; 404 se não existir."""
    if id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return _tarefas[id]


@app.put("/tarefas/{id}")
def atualizar(id: int, tarefa: TarefaUpdate):
    """Substitui titulo e concluida; 404 se o id não existir."""
    if id not in _tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    _tarefas[id]["titulo"] = tarefa.titulo
    _tarefas[id]["concluida"] = tarefa.concluida
    return _tarefas[id]
