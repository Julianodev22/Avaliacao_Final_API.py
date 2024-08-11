from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# py -3 -m venv .venv
# .venv\scripts\activate


class Cliente(BaseModel):
    id: Optional[int] = 0
    nome: str
    cpf: int
    desc: Optional[str] = None


db_clientes = [
    Cliente(id=1, nome="Juliano", cpf=10000000000),
    Cliente(id=2, nome="André", cpf=20000000000),
    Cliente(id=3, nome="Igor", cpf=30000000000),
    Cliente(id=4, nome="Marcel", cpf=4000000000),
]


@app.get("/")
def home():
    return {"mensagem": "Fila de atendimento by FastAPI"}


@app.get("/fila/")
def posicao_fila():
    return {"cliente": "Sua posição na fila é:"}


@app.get("/fila/posicao/{id}")
def exibir_posicao(id: int):
    return {"produto": [cliente for cliente in db_clientes if cliente.id == id]}


@app.get("/fila/dados{id}")
def exibir_dados():
    return {"clientes": db_clientes}


@app.post("/fila/cliente/", status_code=status.HTTP_201_CREATED)
def inserir_cliente(cliente: Cliente):
    cliente.id = db_clientes[-1].id + 1
    db_clientes.append(cliente)
    return {"mensagem": "Cliente inserido!"}


@app.patch("/fila/atualizar/{id}")
def atualizar_posicao(id: int, cliente: Cliente):
    index = [index for index, cliente in enumerate(
        db_clientes) if cliente.id == id]
    cliente.id = db_clientes[index[0]].id
    db_clientes[index[0]] = cliente
    return {"mensagem": "Cliente atualizado!"}


@app.delete("/fila/remover/{id}")
def remover_cliente(id: int):
    cliente = [cliente for cliente in db_clientes if cliente.id == id]
    db_clientes.remove(cliente[0])
    return {"mensagem": "Cliente removido!"}
