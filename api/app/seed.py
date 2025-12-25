from __future__ import annotations

from app.db import SessaoLocal
from app.models import Item


def executar_seed() -> None:
    with SessaoLocal() as sessao:
        total = sessao.query(Item).count()
        if total == 0:
            sessao.add_all(
                [
                    Item(nome="Floresta urbana"),
                    Item(nome="Curso d'água"),
                    Item(nome="Jardim comunitário"),
                ]
            )
            sessao.commit()


if __name__ == "__main__":
    executar_seed()
