# Nature As a Service (NaaS) — Sistema Operacional Global de Regeneração Ambiental

Este repositório contém o MVP completo do NaaS, com frontend, backend, banco de dados e jobs assíncronos.

## Visão geral
- Frontend: Next.js (App Router) + TypeScript + TailwindCSS + Leaflet
- Backend: FastAPI + SQLAlchemy + Pydantic + Alembic
- Banco: PostgreSQL (Docker)
- Jobs: Redis + RQ
- Autenticação: Argon2 + JWT (access/refresh) + RBAC

## Como executar

### Pré-requisitos
- Docker
- Docker Compose

### Subir ambiente
```bash
cd naas-platform
docker compose -f infra/docker-compose.yml up --build
```

### Acessos
- Frontend: http://localhost:3000
- Backend (OpenAPI): http://localhost:8000/docs

## Testes
```bash
cd naas-platform/apps/api
pytest
```

## Estrutura
```
/naas-platform
  /apps/web        → Next.js
  /apps/api        → FastAPI
  /infra           → docker-compose.yml
  /docs
    arquitetura.md
    api.md
    manual_prefeituras.md
```

## Observações
- Este MVP usa dados simulados e seeds automáticas.
- Não há blockchain nem token real. As Unidades de Impacto são internas.
