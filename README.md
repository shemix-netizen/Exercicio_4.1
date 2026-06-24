# Exercício 4.1 — API REST de TODO List

Módulo 3 — Construindo interfaces (Aula 6: APIs REST).

API REST mínima que serve de backend para uma aplicação de TODO list. Gerencia tarefas
em memória e expõe os três verbos centrais: **POST** (cria), **GET** (lê) e **PUT** (atualiza).

> A ideia da Aula 6: **uma API é um contrato**. Cumprindo o contrato, qualquer cliente —
> o autograder, e no 4.2 o servidor MCP — consome sem saber como foi implementada por dentro.

## Estrutura

```
Exercicio_4.1/
├── app/
│   ├── __init__.py
│   └── main.py            # a API
├── requirements.txt       # fastapi e uvicorn
├── README.md
└── .autograde-exercise    # conteúdo: 4.1
```

## Como rodar

```powershell
cd "C:\Users\Usuario\Documents\Mestrado_Ciencias_de_Dados\Transformacao_digital_do_governo\Exercicio_4.1"
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

A API sobe em `http://localhost:8000`. **Deixe a janela do uvicorn aberta** e rode o
autograder (`autograde validar 4.1`) em outra janela do PowerShell.

## Contrato da API

| Método | Rota            | Corpo de entrada                           | Resposta                                          |
|--------|-----------------|--------------------------------------------|---------------------------------------------------|
| GET    | `/health`       | —                                          | `200 {"status":"ok"}`                             |
| POST   | `/tarefas`      | `{"titulo": "<str>"}`                      | `201 {"id":1,"titulo":"<str>","concluida":false}` |
| GET    | `/tarefas/{id}` | —                                          | `200` a tarefa / `404` se não existe              |
| GET    | `/tarefas`      | —                                          | `200 [ ...tarefas... ]`                           |
| PUT    | `/tarefas/{id}` | `{"titulo": "<str>", "concluida": <bool>}` | `200` tarefa atualizada / `404` se não existe     |

### Recurso tarefa

```json
{ "id": 1, "titulo": "estudar APIs", "concluida": false }
```

### Regras verificadas pelo autograder

- `id` autoincremento começando em **1** (loja vazia → primeiro POST cria `id=1`).
- `concluida` começa **false** no POST.
- O PUT **substitui** `titulo` e `concluida` e devolve a tarefa atualizada.
- Nomes dos campos exatamente: `id`, `titulo`, `concluida` (sem acento, minúsculos).
- Armazenamento **em memória** — zera ao reiniciar (estado limpo proposital).

## Rodando o autograder

1. **Janela 1** — deixe a API no ar (não feche):
   ```powershell
   uvicorn app.main:app --port 8000
   ```
2. **Janela 2** — rode o autograder:
   ```powershell
   autograde validar 4.1
   ```

> ⚠️ O autograder dispara chamadas HTTP reais. Se a API **não** estiver rodando na porta
> 8000, os itens `health`, `post_tarefa`, `get_tarefa` e `put_tarefa` aparecem como
> "não capturado". Garanta o servidor no ar **antes** de validar.

### Solução de problemas

| Sintoma | Causa | Correção |
|---|---|---|
| `comando ... nao capturado` | API fora do ar na 8000 | Suba o `uvicorn` antes de validar |
| POST retorna `id` ≠ 1 | estado sujo de execução anterior | Reinicie o servidor (memória zera) |
| porta 8000 ocupada | processo antigo preso | `netstat -ano \| findstr :8000` e `taskkill /F /PID <pid>` |

## Testando manualmente (PowerShell)

Use `curl.exe` (não o alias `curl`) e variável `$body` para o JSON do PUT:

```powershell
curl.exe -s http://localhost:8000/health

curl.exe -s -X POST http://localhost:8000/tarefas `
  -H "Content-Type: application/json" -d '{\"titulo\":\"estudar APIs\"}'

curl.exe -s http://localhost:8000/tarefas/1

$body = '{"titulo":"estudar APIs REST","concluida":true}'
curl.exe -s -X PUT http://localhost:8000/tarefas/1 `
  -H "Content-Type: application/json" -d $body

curl.exe -s http://localhost:8000/tarefas
```
