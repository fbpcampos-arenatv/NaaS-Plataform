# Arquitetura

## Visão geral
O MVP é dividido em três camadas principais:
- **Web**: Next.js (App Router) com mapas Leaflet e UI para módulos do NaaS.
- **API**: FastAPI com SQLAlchemy, autenticação JWT e RBAC.
- **Infra**: Docker Compose com PostgreSQL e Redis.

## Multitenant
Todas as tabelas operacionais possuem `tenant_id` (referência à organização). Esse campo é aplicado nos filtros da API.

## Auditoria
Todas as ações relevantes geram registros em `LogAuditoria` com hash imutável encadeado.

## Jobs
O worker RQ executa tarefas diárias de risco ambiental e geração de missões preventivas.
