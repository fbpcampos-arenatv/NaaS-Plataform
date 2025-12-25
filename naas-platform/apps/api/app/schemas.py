from pydantic import BaseModel


class TokenResposta(BaseModel):
    token_acesso: str
    token_refresh: str
    tipo: str = "bearer"


class UsuarioLogin(BaseModel):
    email: str
    senha: str


class RankingESI(BaseModel):
    cidade_id: int
    cidade: str
    pontuacao: float


class DetalheCidadeESI(BaseModel):
    cidade_id: int
    cidade: str
    janela_anos: int
    pontuacao: float


class AlertaResposta(BaseModel):
    id: int
    nivel: str
    mensagem: str


class MissaoResposta(BaseModel):
    id: int
    titulo: str
    status: str


class TACResposta(BaseModel):
    id: int
    titulo: str
    status: str
