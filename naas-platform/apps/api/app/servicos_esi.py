from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Cidade, MetricaAmbiental, SerieHistorica, ResultadoESI


CATEGORIAS = [
    "ar",
    "agua",
    "solo",
    "urbano",
    "residuos",
    "queimadas",
    "enchentes",
    "temperatura_solo",
]


def normalizar(valor: float, minimo: float, maximo: float) -> float:
    if maximo == minimo:
        return 0.0
    return max(0.0, min(100.0, (valor - minimo) / (maximo - minimo) * 100))


def calcular_esi(sessao: Session, cidade_id: int, janela_anos: int) -> float:
    metricas = sessao.scalars(select(MetricaAmbiental)).all()
    if not metricas:
        return 0.0
    total_peso = sum(m.peso for m in metricas)
    if total_peso == 0:
        return 0.0
    pontuacao_final = 0.0
    for metrica in metricas:
        series = sessao.scalars(
            select(SerieHistorica)
            .where(SerieHistorica.cidade_id == cidade_id)
            .where(SerieHistorica.metrica_id == metrica.id)
            .order_by(SerieHistorica.ano.desc())
            .limit(janela_anos)
        ).all()
        if not series:
            continue
        valores = [s.valor for s in series]
        minimo, maximo = min(valores), max(valores)
        valor_medio = sum(valores) / len(valores)
        normalizado = normalizar(valor_medio, minimo, maximo)
        pontuacao_final += normalizado * metrica.peso
    escala_1000 = (pontuacao_final / total_peso) * 10
    return round(escala_1000, 2)


def atualizar_resultados(sessao: Session, cidade_id: int, janelas: list[int]) -> list[ResultadoESI]:
    resultados = []
    for janela in janelas:
        pontuacao = calcular_esi(sessao, cidade_id, janela)
        existente = sessao.scalar(
            select(ResultadoESI)
            .where(ResultadoESI.cidade_id == cidade_id)
            .where(ResultadoESI.janela_anos == janela)
        )
        if existente:
            existente.pontuacao = pontuacao
            resultados.append(existente)
        else:
            resultado = ResultadoESI(
                tenant_id=1,
                cidade_id=cidade_id,
                janela_anos=janela,
                pontuacao=pontuacao,
            )
            sessao.add(resultado)
            resultados.append(resultado)
    sessao.commit()
    return resultados
