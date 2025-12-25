from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db import obter_sessao
from app.models import Usuario, PerfilAcesso
from app.settings import configuracoes

contexto_senha = CryptContext(schemes=["argon2"], deprecated="auto")

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def gerar_hash_senha(senha: str) -> str:
    return contexto_senha.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return contexto_senha.verify(senha, senha_hash)


def criar_token(dados: dict, expira_em: timedelta) -> str:
    dados_para_token = dados.copy()
    dados_para_token["exp"] = datetime.utcnow() + expira_em
    return jwt.encode(dados_para_token, configuracoes.chave_jwt, algorithm=configuracoes.algoritmo_jwt)


def criar_access_token(usuario_id: int, perfil: str) -> str:
    return criar_token(
        {"sub": str(usuario_id), "perfil": perfil},
        timedelta(minutes=configuracoes.jwt_expira_minutos),
    )


def criar_refresh_token(usuario_id: int) -> str:
    return criar_token(
        {"sub": str(usuario_id), "tipo": "refresh"},
        timedelta(days=configuracoes.jwt_refresh_expira_dias),
    )


def obter_usuario_por_token(
    token: str = Depends(esquema_oauth2),
    sessao: Session = Depends(obter_sessao),
) -> Usuario:
    try:
        dados_token = jwt.decode(token, configuracoes.chave_jwt, algorithms=[configuracoes.algoritmo_jwt])
        usuario_id = int(dados_token.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    usuario = sessao.get(Usuario, usuario_id)
    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inválido")
    return usuario


def exigir_perfil(perfis_permitidos: list[str]):
    def verificador(usuario: Usuario = Depends(obter_usuario_por_token), sessao: Session = Depends(obter_sessao)) -> Usuario:
        perfil = sessao.get(PerfilAcesso, usuario.perfil_id)
        if not perfil or perfil.nome not in perfis_permitidos:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        return usuario

    return verificador
