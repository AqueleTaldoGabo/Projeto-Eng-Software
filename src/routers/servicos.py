from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from src import schemas
from src.entities.Servico import Servico

router = APIRouter(
    prefix='/servicos',
    tags=['Serviços']
)

@router.get('/', response_model=List[schemas.ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    servicos = db.query(Servico).all()
    return servicos


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ServicoResponse)
def criar_servico(servico_in: schemas.ServicoCreate, db: Session = Depends(get_db)):
    novo_servico = Servico(**servico_in.dict())
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)
    return novo_servico


@router.get('/{id}', response_model=schemas.ServicoResponse, status_code=status.HTTP_200_OK)
def buscar_servico_por_id(id: int, db: Session = Depends(get_db)):
    servico = db.query(Servico).filter(Servico.id == id).first()

    if servico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"O id: {id} solicitado não existe"
        )
    return servico


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(id: int, db: Session = Depends(get_db)):
    query_deletar = db.query(Servico).filter(Servico.id == id)

    if query_deletar.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O id: {id} solicitado não existe"
        )
        
    query_deletar.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', response_model=schemas.ServicoResponse)
def atualizar_servico(update_dados: schemas.ServicoBase, id: int, db: Session = Depends(get_db)):
    query_atualizar = db.query(Servico).filter(Servico.id == id)

    if query_atualizar.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"O id: {id} solicitado não existe"
        )
        
    query_atualizar.update(update_dados.dict(), synchronize_session=False)
    db.commit()

    return query_atualizar.first()