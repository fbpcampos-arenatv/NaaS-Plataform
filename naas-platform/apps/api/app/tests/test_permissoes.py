import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth import exigir_perfil
from app.db import BaseDeclarativa
from app.models import PerfilAcesso, Usuario


def test_perfil_permitido():
    motor = create_engine("sqlite:///:memory:", future=True)
    BaseDeclarativa.metadata.create_all(bind=motor)
    Sessao = sessionmaker(bind=motor)

    with Sessao() as sessao:
        perfil = PerfilAcesso(tenant_id=1, nome="AdministradorGlobal")
        usuario = Usuario(
            tenant_id=1,
            nome="Teste",
            email="teste@naas.local",
            senha_hash="hash",
            perfil_id=1,
        )
        sessao.add(perfil)
        sessao.add(usuario)
        sessao.commit()

        verificador = exigir_perfil(["AdministradorGlobal"])
        assert verificador(usuario=usuario, sessao=sessao) == usuario


def test_perfil_negado():
    motor = create_engine("sqlite:///:memory:", future=True)
    BaseDeclarativa.metadata.create_all(bind=motor)
    Sessao = sessionmaker(bind=motor)

    with Sessao() as sessao:
        perfil = PerfilAcesso(tenant_id=1, nome="Cidadao")
        usuario = Usuario(
            tenant_id=1,
            nome="Teste",
            email="teste2@naas.local",
            senha_hash="hash",
            perfil_id=1,
        )
        sessao.add(perfil)
        sessao.add(usuario)
        sessao.commit()

        verificador = exigir_perfil(["AdministradorGlobal"])
        with pytest.raises(Exception):
            verificador(usuario=usuario, sessao=sessao)
