from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import exigir_perfil
from app.db import obter_sessao
from app.models import TAC
from app.schemas import TACResposta

roteador = APIRouter(prefix="/tac", tags=["TAC"])


@roteador.get("", response_model=list[TACResposta])
def listar_tacs(
    sessao: Session = Depends(obter_sessao),
    _usuario=Depends(exigir_perfil(["AdministradorGlobal", "GestorMunicipal", "Auditor", "EmpresaParceira"])),
) -> list[TACResposta]:
    tacs = sessao.scalars(select(TAC)).all()
    return [TACResposta(id=t.id, titulo=t.titulo, status=t.status) for t in tacs]


@roteador.get("/{tac_id}", response_model=TACResposta)
def detalhe_tac(
    tac_id: int,
    sessao: Session = Depends(obter_sessao),
    _usuario=Depends(exigir_perfil(["AdministradorGlobal", "GestorMunicipal", "Auditor", "EmpresaParceira"])),
) -> TACResposta:
    tac = sessao.get(TAC, tac_id)
    if not tac:
        return TACResposta(id=0, titulo="Não encontrado", status="Inexistente")
    return TACResposta(id=tac.id, titulo=tac.titulo, status=tac.status)
