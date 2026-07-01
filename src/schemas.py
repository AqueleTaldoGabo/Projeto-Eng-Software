from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class ServicoBase(BaseModel):
    descricao: str
    preco: float
    tempo_estimado: str
    status: str


class ServicoCreate(ServicoBase):
    prestador_id: int  

class ServicoResponse(ServicoBase):
    id: int
    avaliacao: float
    quantavaliacao: int
    created_at: datetime

    class Config:
        from_attributes = True


class PrestadorBase(BaseModel):
    nome: str
    email: str 
    telefone: str
    localizacao: str

class PrestadorCreate(PrestadorBase):
    senha: str

class PrestadorResponse(PrestadorBase):
    id: int
    created_at: datetime
    
    servicos: List[ServicoResponse] = []

    class Config:
        from_attributes = True


class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: str
    localizacao: str

class ClienteCreate(ClienteBase):
    senha: str

class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AvaliacaoInput(BaseModel):
    nota: float 

class SchemaLogin(BaseModel):
    email: EmailStr  
    senha: str