from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import exigir_perfil
from app.db import obter_sessao
from app.models import Alerta, RiscoAmbiental, Missao
from app.schemas import AlertaResposta, MissaoResposta

roteador = APIRouter(prefix="/brigadas", tags=["Brigadas"])


@roteador.get("/alertas", response_model=list[AlertaResposta])
def listar_alertas(
    sessao: Session = Depends(obter_sessao),
    _usuario=Depends(exigir_perfil(["AdministradorGlobal", "GestorMunicipal", "Auditor"])),
) -> list[AlertaResposta]:
    alertas = sessao.scalars(select(Alerta).where(Alerta.ativo == True)).all()
    respostas = []
    for alerta in alertas:
        risco = sessao.get(RiscoAmbiental, alerta.risco_id)
        nivel = risco.nivel if risco else "Amarelo"
        respostas.append(AlertaResposta(id=alerta.id, nivel=nivel, mensagem=alerta.mensagem))
    return respostas


@roteador.get("/missoes", response_model=list[MissaoResposta])
def listar_missoes(
    sessao: Session = Depends(obter_sessao),
    _usuario=Depends(exigir_perfil(["AdministradorGlobal", "GestorMunicipal", "Auditor"])),
) -> list[MissaoResposta]:
    missoes = sessao.scalars(select(Missao)).all()
    return [MissaoResposta(id=m.id, titulo=m.titulo, status=m.status) for m in missoes]
