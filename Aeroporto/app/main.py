from fastapi import FastAPI
from .routers import portao_router, voo_router, passageiro_router

app = FastAPI(title="API do Aeroporto")
app.include_router(portao_router)
app.include_router(voo_router)
app.include_router(passageiro_router)
