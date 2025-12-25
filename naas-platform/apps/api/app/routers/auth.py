from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.auth import criar_access_token, criar_refresh_token, verificar_senha
from app.db import obter_sessao
from app.models import Usuario, PerfilAcesso
from app.schemas import TokenResposta, UsuarioLogin

roteador = APIRouter(prefix="/auth", tags=["Autenticação"])


@roteador.post("/login", response_model=TokenResposta)
def login(dados: UsuarioLogin, sessao: Session = Depends(obter_sessao)) -> TokenResposta:
    usuario = sessao.scalar(select(Usuario).where(Usuario.email == dados.email))
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    perfil = sessao.get(PerfilAcesso, usuario.perfil_id)
    token_acesso = criar_access_token(usuario.id, perfil.nome if perfil else "Cidadao")
    token_refresh = criar_refresh_token(usuario.id)
    return TokenResposta(token_acesso=token_acesso, token_refresh=token_refresh)


@roteador.post("/refresh", response_model=TokenResposta)
def refresh(token: str, sessao: Session = Depends(obter_sessao)) -> TokenResposta:
    usuario = sessao.scalar(select(Usuario).where(Usuario.id == int(token)))
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    perfil = sessao.get(PerfilAcesso, usuario.perfil_id)
    token_acesso = criar_access_token(usuario.id, perfil.nome if perfil else "Cidadao")
    token_refresh = criar_refresh_token(usuario.id)
    return TokenResposta(token_acesso=token_acesso, token_refresh=token_refresh)
