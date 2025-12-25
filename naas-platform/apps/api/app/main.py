from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import BaseDeclarativa, motor, SessaoLocal
from app.seed import seed_dados
from app.routers import auth, esi, brigadas, tac

app = FastAPI(title="NaaS API", description="API do MVP NaaS", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

app.include_router(auth.roteador)
app.include_router(esi.roteador)
app.include_router(brigadas.roteador)
app.include_router(tac.roteador)


@app.on_event("startup")
def iniciar_banco():
    BaseDeclarativa.metadata.create_all(bind=motor)
    with SessaoLocal() as sessao:
        seed_dados(sessao)


@app.get("/")
def raiz():
    return {"mensagem": "NaaS API ativa"}
