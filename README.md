# Nature As a Service (NaaS) – INICIANTE TOTAL

Este repositório contém:
- **Web**: Next.js (porta 3000)
- **API**: FastAPI (porta 8000, com `/docs`)
- **Banco**: PostgreSQL
- **Fila/Jobs**: Redis

## Pré-requisitos
- Docker Desktop instalado e rodando
- Git instalado

## Passo a passo (copiar e colar)

```bash
git clone <URL_DO_REPOSITORIO>
cd NaaS-Plataform

docker compose up --build
```

## Como confirmar que está no ar
1. **Web**: abra http://localhost:3000
2. **API**: abra http://localhost:8000/health
3. **Docs**: abra http://localhost:8000/docs

Se tudo estiver ok, a página da Web mostrará os itens de exemplo vindos da API.

## Migrações e seed automáticos
- As migrações do Alembic rodam automaticamente no startup do container da API.
- Um seed inicial cria registros de exemplo na tabela `itens`.

## Solução de problemas (erros comuns)

1) **Erro: `docker: command not found`**
- Instale o Docker Desktop e reinicie o terminal.
- Verifique se o comando `docker --version` funciona.

2) **Porta já em uso (3000/8000/5432/6379)**
- Feche o serviço que está usando a porta ou altere o mapeamento em `docker-compose.yml`.
- Depois reinicie: `docker compose up --build`.

3) **API não conecta no banco**
- Aguarde alguns segundos: o container tenta conectar por até ~1 minuto.
- Se persistir, apague volumes antigos: `docker compose down -v` e suba novamente.

---

## Checklist de verificação
1. Verificar estrutura e stack (Next.js, FastAPI, Postgres, Redis/Jobs).
2. Rodar `docker compose up --build`.
3. Confirmar Web em http://localhost:3000 e API em http://localhost:8000 com `/docs` funcionando.
4. Garantir migrações automáticas e seed inicial.
5. Validar README “INICIANTE TOTAL” com passos e troubleshooting.
6. Manter tudo em português e registrar as correções.
