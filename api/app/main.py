from __future__ import annotations

from fastapi import FastAPI

from app.db import SessaoLocal
from app.models import Item

app = FastAPI(title="NaaS API")


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.get("/itens")
def listar_itens() -> list[dict]:
    with SessaoLocal() as sessao:
        itens = sessao.query(Item).order_by(Item.id).all()
        return [
            {"id": item.id, "nome": item.nome, "criado_em": item.criado_em.isoformat()}
            for item in itens
        ]
