from pydantic_settings import BaseSettings


class Configuracoes(BaseSettings):
    url_banco: str = "sqlite:///./naas.db"
    url_redis: str = "redis://localhost:6379/0"
    chave_jwt: str = "chave-super-secreta"
    algoritmo_jwt: str = "HS256"
    jwt_expira_minutos: int = 30
    jwt_refresh_expira_dias: int = 7


configuracoes = Configuracoes()
