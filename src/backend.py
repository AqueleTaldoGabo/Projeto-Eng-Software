from fastapi import FastAPI
from src.database import engine, Base  
from src.entities.Prestador import Prestador
from src.entities.Servico import Servico
from src.entities.Cliente import Cliente

from src.routers import prestadores, clientes, servicos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Engenharia de Software API")

app.include_router(clientes.router)
app.include_router(prestadores.router)
app.include_router(servicos.router)

@app.get("/")
def root():
    return {"message": "Ta funcionando?"}