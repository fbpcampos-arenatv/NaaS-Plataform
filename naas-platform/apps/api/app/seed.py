from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import gerar_hash_senha
from app.models import (
    Alerta,
    Brigada,
    CaminhaoPipa,
    Cidade,
    Conselho,
    DecisaoConselho,
    LogAuditoria,
    MarcoProjeto,
    MetricaAmbiental,
    Missao,
    ModeloProjeto,
    Organizacao,
    ParteResponsavel,
    PeriodoCritico,
    PerfilAcesso,
    Projeto,
    RelatorioVerificacao,
    RiscoAmbiental,
    SerieHistorica,
    TAC,
    TurnoBrigada,
    Usuario,
)
from app.servicos_esi import atualizar_resultados, CATEGORIAS


def registrar_log(sessao: Session, acao: str, entidade: str, entidade_id: int, hash_anterior: str) -> LogAuditoria:
    hash_atual = f"{hash_anterior}:{acao}:{entidade}:{entidade_id}"
    log = LogAuditoria(
        tenant_id=1,
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        hash_anterior=hash_anterior,
        hash_atual=hash_atual,
    )
    sessao.add(log)
    return log


def seed_dados(sessao: Session) -> None:
    if sessao.scalar(select(Organizacao)):
        return

    organizacao = Organizacao(tenant_id=1, nome="NaaS Global", tipo="Plataforma")
    sessao.add(organizacao)

    perfis = [
        "AdministradorGlobal",
        "GestorMunicipal",
        "Auditor",
        "EmpresaParceira",
        "Cidadao",
    ]
    perfis_obj = []
    for nome in perfis:
        perfis_obj.append(PerfilAcesso(tenant_id=1, nome=nome))
    sessao.add_all(perfis_obj)
    sessao.flush()

    usuario_admin = Usuario(
        tenant_id=1,
        nome="Admin Global",
        email="admin@naas.local",
        senha_hash=gerar_hash_senha("admin123"),
        perfil_id=perfis_obj[0].id,
    )
    sessao.add(usuario_admin)

    cidades = [
        Cidade(tenant_id=1, nome="Manaus", pais="Brasil", populacao=2200000),
        Cidade(tenant_id=1, nome="Vancouver", pais="Canadá", populacao=675000),
    ]
    sessao.add_all(cidades)
    sessao.flush()

    metricas = [
        MetricaAmbiental(tenant_id=1, categoria=categoria, unidade="índice", peso=1.0)
        for categoria in CATEGORIAS
    ]
    sessao.add_all(metricas)
    sessao.flush()

    ano_atual = datetime.utcnow().year
    for cidade in cidades:
        for metrica in metricas:
            for i in range(1, 31):
                sessao.add(
                    SerieHistorica(
                        tenant_id=1,
                        cidade_id=cidade.id,
                        metrica_id=metrica.id,
                        ano=ano_atual - i,
                        valor=50 + (i % 10) * 2,
                    )
                )

    periodo = PeriodoCritico(
        tenant_id=1,
        cidade_id=cidades[0].id,
        descricao="Período crítico de queimadas",
        inicio=date.today(),
        fim=date.today() + timedelta(days=90),
    )
    sessao.add(periodo)

    risco = RiscoAmbiental(
        tenant_id=1,
        cidade_id=cidades[0].id,
        nivel="Laranja",
        detalhe="Risco elevado de incêndios",
    )
    sessao.add(risco)
    sessao.flush()

    alerta = Alerta(tenant_id=1, risco_id=risco.id, mensagem="Monitoramento reforçado", ativo=True)
    sessao.add(alerta)

    brigada = Brigada(tenant_id=1, cidade_id=cidades[0].id, nome="Brigada Amazônia", ativa=True)
    sessao.add(brigada)
    sessao.flush()

    turno = TurnoBrigada(
        tenant_id=1,
        brigada_id=brigada.id,
        inicio=datetime.utcnow(),
        fim=datetime.utcnow() + timedelta(hours=8),
    )
    sessao.add(turno)
    sessao.add(CaminhaoPipa(tenant_id=1, brigada_id=brigada.id, identificador="CP-01"))

    missao = Missao(
        tenant_id=1,
        brigada_id=brigada.id,
        titulo="Patrulha preventiva",
        status="Ativa",
    )
    sessao.add(missao)

    tac = TAC(
        tenant_id=1,
        cidade_id=cidades[0].id,
        titulo="TAC Floresta Viva",
        status="Em execução",
    )
    sessao.add(tac)
    sessao.flush()

    sessao.add(ParteResponsavel(tenant_id=1, tac_id=tac.id, nome="Empresa X"))

    modelo = ModeloProjeto(tenant_id=1, nome="Reflorestamento", descricao="Modelo padrão")
    sessao.add(modelo)

    projeto1 = Projeto(tenant_id=1, cidade_id=cidades[0].id, nome="Projeto Rio Limpo", status="Em andamento")
    projeto2 = Projeto(tenant_id=1, cidade_id=cidades[1].id, nome="Projeto Serra Verde", status="Planejamento")
    sessao.add_all([projeto1, projeto2])
    sessao.flush()

    sessao.add(MarcoProjeto(tenant_id=1, projeto_id=projeto1.id, descricao="Plantio inicial", concluido=True))
    sessao.add(RelatorioVerificacao(tenant_id=1, projeto_id=projeto1.id, aprovado=True, observacao="Verificação aprovada"))

    conselhos = [
        Conselho(tenant_id=1, tipo="Científico"),
        Conselho(tenant_id=1, tipo="Jurídico"),
        Conselho(tenant_id=1, tipo="Auditoria"),
    ]
    sessao.add_all(conselhos)
    sessao.flush()

    for conselho in conselhos[:2]:
        sessao.add(DecisaoConselho(tenant_id=1, conselho_id=conselho.id, projeto_id=projeto1.id, aprovado=True))

    sessao.flush()

    atualizar_resultados(sessao, cidades[0].id, [5, 10, 20, 30])
    atualizar_resultados(sessao, cidades[1].id, [5, 10, 20, 30])

    registrar_log(sessao, "semente", "organização", organizacao.id, "inicio")
    sessao.commit()
