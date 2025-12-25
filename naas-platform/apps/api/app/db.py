from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.settings import configuracoes


class BaseDeclarativa(DeclarativeBase):
    pass


motor = create_engine(configuracoes.url_banco, future=True)
SessaoLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False)


def obter_sessao():
    sessao = SessaoLocal()
    try:
        yield sessao
    finally:
        sessao.close()
