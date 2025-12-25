from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import exigir_perfil
from app.db import obter_sessao
from app.models import Cidade, ResultadoESI
from app.schemas import DetalheCidadeESI, RankingESI

roteador = APIRouter(prefix="/esi", tags=["ESI-1000"])


@roteador.get("/ranking", response_model=list[RankingESI])
def ranking(sessao: Session = Depends(obter_sessao)) -> list[RankingESI]:
    resultados = sessao.scalars(select(ResultadoESI).where(ResultadoESI.janela_anos == 10)).all()
    respostas = []
    for resultado in resultados:
        cidade = sessao.get(Cidade, resultado.cidade_id)
        if cidade:
            respostas.append(
                RankingESI(cidade_id=cidade.id, cidade=cidade.nome, pontuacao=resultado.pontuacao)
            )
    return sorted(respostas, key=lambda item: item.pontuacao, reverse=True)


@roteador.get("/cidades/{cidade_id}", response_model=list[DetalheCidadeESI])
def detalhe_cidade(
    cidade_id: int,
    sessao: Session = Depends(obter_sessao),
    _usuario=Depends(exigir_perfil(["AdministradorGlobal", "GestorMunicipal", "Auditor", "Cidadao"])),
) -> list[DetalheCidadeESI]:
    resultados = sessao.scalars(select(ResultadoESI).where(ResultadoESI.cidade_id == cidade_id)).all()
    cidade = sessao.get(Cidade, cidade_id)
    if not cidade:
        return []
    return [
        DetalheCidadeESI(
            cidade_id=cidade_id,
            cidade=cidade.nome,
            janela_anos=r.janela_anos,
            pontuacao=r.pontuacao,
        )
        for r in resultados
    ]
