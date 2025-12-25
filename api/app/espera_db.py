from __future__ import annotations

import os
import time

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

for tentativa in range(1, 31):
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
        print("Banco de dados disponível.")
        break
    except Exception as erro:  # noqa: BLE001
        print(f"Tentativa {tentativa}/30 falhou: {erro}")
        time.sleep(2)
else:
    raise SystemExit("Banco de dados não respondeu a tempo.")
