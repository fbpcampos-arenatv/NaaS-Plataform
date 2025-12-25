from datetime import datetime
import time

from redis import Redis
from rq import Queue
from sqlalchemy import select

from app.db import SessaoLocal
from app.models import Cidade, RiscoAmbiental, Alerta, Missao, Brigada
from app.settings import configuracoes


def gerar_risco_diario():
    with SessaoLocal() as sessao:
        cidades = sessao.scalars(select(Cidade)).all()
        for cidade in cidades:
            risco = RiscoAmbiental(
                tenant_id=cidade.tenant_id,
                cidade_id=cidade.id,
                nivel="Amarelo",
                detalhe="Risco gerado automaticamente",
            )
            sessao.add(risco)
            sessao.flush()
            alerta = Alerta(
                tenant_id=cidade.tenant_id,
                risco_id=risco.id,
                mensagem="Alerta automático diário",
                ativo=True,
            )
            sessao.add(alerta)
            brigada = sessao.scalar(select(Brigada).where(Brigada.cidade_id == cidade.id))
            if brigada:
                missao = Missao(
                    tenant_id=cidade.tenant_id,
                    brigada_id=brigada.id,
                    titulo=f"Missão preventiva {datetime.utcnow().date()}",
                    status="Ativa",
                )
                sessao.add(missao)
        sessao.commit()


if __name__ == "__main__":
    conexao_redis = Redis.from_url(configuracoes.url_redis)
    fila = Queue("naas", connection=conexao_redis)
    while True:
        fila.enqueue(gerar_risco_diario)
        time.sleep(86400)
