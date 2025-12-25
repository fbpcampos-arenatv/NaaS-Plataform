from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import BaseDeclarativa
from app.models import Cidade, MetricaAmbiental, SerieHistorica
from app.servicos_esi import calcular_esi


def test_calculo_esi_basico():
    motor = create_engine("sqlite:///:memory:", future=True)
    BaseDeclarativa.metadata.create_all(bind=motor)
    Sessao = sessionmaker(bind=motor)

    with Sessao() as sessao:
        cidade = Cidade(tenant_id=1, nome="Teste", pais="Brasil", populacao=1000)
        sessao.add(cidade)
        sessao.flush()
        metrica = MetricaAmbiental(tenant_id=1, categoria="ar", unidade="índice", peso=1.0)
        sessao.add(metrica)
        sessao.flush()
        sessao.add_all(
            [
                SerieHistorica(tenant_id=1, cidade_id=cidade.id, metrica_id=metrica.id, ano=2020, valor=10),
                SerieHistorica(tenant_id=1, cidade_id=cidade.id, metrica_id=metrica.id, ano=2021, valor=20),
            ]
        )
        sessao.commit()

        pontuacao = calcular_esi(sessao, cidade.id, 2)
        assert pontuacao >= 0
