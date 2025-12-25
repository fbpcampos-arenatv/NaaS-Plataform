from datetime import datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import BaseDeclarativa


class BaseComum(BaseDeclarativa):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(Integer, index=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Organizacao(BaseComum):
    __tablename__ = "organizacoes"
    nome: Mapped[str] = mapped_column(String(200))
    tipo: Mapped[str] = mapped_column(String(50))


class PerfilAcesso(BaseComum):
    __tablename__ = "perfis_acesso"
    nome: Mapped[str] = mapped_column(String(100))


class Usuario(BaseComum):
    __tablename__ = "usuarios"
    nome: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    perfil_id: Mapped[int] = mapped_column(ForeignKey("perfis_acesso.id"))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class Cidade(BaseComum):
    __tablename__ = "cidades"
    nome: Mapped[str] = mapped_column(String(200))
    pais: Mapped[str] = mapped_column(String(100))
    populacao: Mapped[int] = mapped_column(Integer)


class Regiao(BaseComum):
    __tablename__ = "regioes"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    nome: Mapped[str] = mapped_column(String(200))


class MetricaAmbiental(BaseComum):
    __tablename__ = "metricas_ambientais"
    categoria: Mapped[str] = mapped_column(String(100))
    unidade: Mapped[str] = mapped_column(String(50))
    peso: Mapped[float] = mapped_column(Float, default=1.0)


class SerieHistorica(BaseComum):
    __tablename__ = "series_historicas"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    metrica_id: Mapped[int] = mapped_column(ForeignKey("metricas_ambientais.id"))
    ano: Mapped[int] = mapped_column(Integer)
    valor: Mapped[float] = mapped_column(Float)


class ResultadoESI(BaseComum):
    __tablename__ = "resultados_esi"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    janela_anos: Mapped[int] = mapped_column(Integer)
    pontuacao: Mapped[float] = mapped_column(Float)


class PeriodoCritico(BaseComum):
    __tablename__ = "periodos_criticos"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    descricao: Mapped[str] = mapped_column(String(200))
    inicio: Mapped[Date] = mapped_column(Date)
    fim: Mapped[Date] = mapped_column(Date)


class RiscoAmbiental(BaseComum):
    __tablename__ = "riscos_ambientais"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    nivel: Mapped[str] = mapped_column(String(50))
    detalhe: Mapped[str] = mapped_column(String(200))


class Alerta(BaseComum):
    __tablename__ = "alertas"
    risco_id: Mapped[int] = mapped_column(ForeignKey("riscos_ambientais.id"))
    mensagem: Mapped[str] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class Brigada(BaseComum):
    __tablename__ = "brigadas"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    nome: Mapped[str] = mapped_column(String(200))
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)


class TurnoBrigada(BaseComum):
    __tablename__ = "turnos_brigada"
    brigada_id: Mapped[int] = mapped_column(ForeignKey("brigadas.id"))
    inicio: Mapped[DateTime] = mapped_column(DateTime)
    fim: Mapped[DateTime] = mapped_column(DateTime)


class Drone(BaseComum):
    __tablename__ = "drones"
    brigada_id: Mapped[int] = mapped_column(ForeignKey("brigadas.id"))
    identificador: Mapped[str] = mapped_column(String(100))


class CaminhaoPipa(BaseComum):
    __tablename__ = "caminhoes_pipa"
    brigada_id: Mapped[int] = mapped_column(ForeignKey("brigadas.id"))
    identificador: Mapped[str] = mapped_column(String(100))


class Missao(BaseComum):
    __tablename__ = "missoes"
    brigada_id: Mapped[int] = mapped_column(ForeignKey("brigadas.id"))
    titulo: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50))


class EventoMissao(BaseComum):
    __tablename__ = "eventos_missao"
    missao_id: Mapped[int] = mapped_column(ForeignKey("missoes.id"))
    tipo: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[str] = mapped_column(String(255))


class TAC(BaseComum):
    __tablename__ = "tacs"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    titulo: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50))


class ParteResponsavel(BaseComum):
    __tablename__ = "partes_responsaveis"
    tac_id: Mapped[int] = mapped_column(ForeignKey("tacs.id"))
    nome: Mapped[str] = mapped_column(String(200))


class ObrigacaoAmbiental(BaseComum):
    __tablename__ = "obrigacoes_ambientais"
    tac_id: Mapped[int] = mapped_column(ForeignKey("tacs.id"))
    descricao: Mapped[str] = mapped_column(Text)


class Projeto(BaseComum):
    __tablename__ = "projetos"
    cidade_id: Mapped[int] = mapped_column(ForeignKey("cidades.id"))
    nome: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50))


class MarcoProjeto(BaseComum):
    __tablename__ = "marcos_projeto"
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projetos.id"))
    descricao: Mapped[str] = mapped_column(String(200))
    concluido: Mapped[bool] = mapped_column(Boolean, default=False)


class RelatorioVerificacao(BaseComum):
    __tablename__ = "relatorios_verificacao"
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projetos.id"))
    aprovado: Mapped[bool] = mapped_column(Boolean, default=False)
    observacao: Mapped[str] = mapped_column(Text)


class ModeloProjeto(BaseComum):
    __tablename__ = "modelos_projeto"
    nome: Mapped[str] = mapped_column(String(200))
    descricao: Mapped[str] = mapped_column(Text)


class CompromissoFinanceiro(BaseComum):
    __tablename__ = "compromissos_financeiros"
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projetos.id"))
    valor: Mapped[float] = mapped_column(Float)
    apoiador: Mapped[str] = mapped_column(String(200))


class LivroImpacto(BaseComum):
    __tablename__ = "livro_impacto"
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projetos.id"))
    unidades: Mapped[float] = mapped_column(Float)
    descricao: Mapped[str] = mapped_column(String(200))


class Conselho(BaseComum):
    __tablename__ = "conselhos"
    tipo: Mapped[str] = mapped_column(String(100))


class DecisaoConselho(BaseComum):
    __tablename__ = "decisoes_conselho"
    conselho_id: Mapped[int] = mapped_column(ForeignKey("conselhos.id"))
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projetos.id"))
    aprovado: Mapped[bool] = mapped_column(Boolean, default=False)


class Politica(BaseComum):
    __tablename__ = "politicas"
    nome: Mapped[str] = mapped_column(String(200))
    descricao: Mapped[str] = mapped_column(Text)


class LogAuditoria(BaseComum):
    __tablename__ = "logs_auditoria"
    acao: Mapped[str] = mapped_column(String(200))
    entidade: Mapped[str] = mapped_column(String(100))
    entidade_id: Mapped[int] = mapped_column(Integer)
    hash_anterior: Mapped[str] = mapped_column(String(255))
    hash_atual: Mapped[str] = mapped_column(String(255))
