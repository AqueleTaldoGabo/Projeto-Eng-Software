from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse 
from fastapi.templating import Jinja2Templates 
from fastapi.staticfiles import StaticFiles 

from src.database import engine, Base  
from src.entities.Prestador import Prestador
from src.entities.Servico import Servico
from src.entities.Cliente import Cliente


from src.routers import prestadores, clientes, servicos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Engenharia de Software API")

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

app.include_router(clientes.router)
app.include_router(prestadores.router)
app.include_router(servicos.router)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={}  
    )