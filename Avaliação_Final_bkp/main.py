from fastapi import FastAPI, HTTPException, Query
from datetime import date
from typing import Optional
from pydantic import BaseModel
from typing import Optional

# py -3 -m venv .venv
# .venv\scripts\activate

app = FastAPI()


class Cliente(BaseModel):
    id: Optional[int] = 0
    nome: str
    cpf: int
    desc: Optional[str] = None


data = date.today()
cliente = [{"nome": "Vazio",
            "data": f"{data.day}/{data.month}/{data.year}", "atendido": "Vazio"}]
cliente.append({"nome": "Juliano",
                "data": f"{data.day}/{data.month}/{data.year}", "atendido": False})
cliente.append({"nome": "Juliana",
                "data": f"{data.day}/{data.month}/{data.year}", "atendido": False})
cliente.append({"nome": "Ana",
                "data": f"{data.day}/{data.month}/{data.year}", "atendido": False})
cliente.append({"nome": "André",
                "data": f"{data.day}/{data.month}/{data.year}", "atendido": False})


@app.get("/")
def index():
    return {"mensagem": "Fila de atendimento byFastAPI"}


@app.get("/fila")
def exibir_Fila():
    aux = []
    if len(cliente) == 1:
        raise HTTPException(status_code=200)
    else:
        for n in cliente:
            if cliente.index(n) == 0:
                pass
            else:
                aux.append({"Posição": cliente.index(
                    n), "Nome": n['nome'], "Data": n['data'], "atendido": n['atendido']})
        return aux


@app.get("/fila/{id:int}")
def exibir_Posicao_Fila(id):
    for n in cliente:
        if cliente.index(n) == id:
            return {"Posição": cliente.index(n), "Nome": n['nome'], "Data": n['data'], "atendido": n['atendido']}
        else:
            pass
    raise HTTPException(
        status_code=404, detail="O ID não foi encontrado! :(")


@app.post("/fila")
def inserir_Cliente(nome: str = Query(max_length=20)):
    aux = len(cliente)
    cliente.append(
        {"nome": nome, "data": f"{data.day}/{data.month}/{data.year}", "atendido": False})
    return {"Adicionado": {"Posição": aux, "nome": nome, "data": f"{data.day}/{data.month}/{data.year}", "atendido": False}}


@app.put("/fila")
def atender_Cliente():
    if len(cliente) == 1:
        return {"mensagem": "Fila vazia!"}
    else:
        del (cliente[0])
        cliente[0]["atendido"] = True
        return {"mensagem": "O primeiro cliente da fila está sendo atendido!"}


@app.delete("/fila/{id:int}")
def remover_Cliente(id):
    try:
        if cliente[id]:
            del (cliente[id])
            return {"mensagem": f"O ID '{id}' foi removido da fila!"}
    except (IndexError):
        raise HTTPException(
            status_code=404, detail="O ID não foi encontrado :(")
