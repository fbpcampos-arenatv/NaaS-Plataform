#!/usr/bin/env bash
set -euo pipefail

echo "Aguardando banco de dados..."
python app/espera_db.py

echo "Rodando migrações..."
alembic upgrade head

echo "Aplicando seed inicial..."
python app/seed.py

echo "Iniciando API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
