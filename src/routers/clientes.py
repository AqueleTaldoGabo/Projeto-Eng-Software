from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from src import schemas
from src.entities.Prestador import Prestador

router = APIRouter(
    prefix='/prestadores',
    tags=['Prestadores']
)

@router.get('/', response_model=List[schemas.PrestadorResponse])
def listar_prestadores(db: Session = Depends(get_db)):
    prestadores = db.query(Prestador).all()
    return prestadores

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PrestadorResponse)
def criar_prestador(prestador_in: schemas.PrestadorCreate, db: Session = Depends(get_db)):
    email_existente = db.query(Prestador).filter(Prestador.email == prestador_in.email).first()
    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este e-mail já está cadastrado."
        )

    novo_prestador = Prestador(**prestador_in.dict())
    db.add(novo_prestador)
    db.commit()
    db.refresh(novo_prestador)
    return novo_prestador

@router.get('/{id}', response_model=schemas.PrestadorResponse, status_code=status.HTTP_200_OK)
def buscar_prestador_por_id(id: int, db: Session = Depends(get_db)):
    prestador = db.query(Prestador).filter(Prestador.id == id).first()
    if prestador is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"O prestador com id: {id} não existe"
        )
    return prestador

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_prestador(id: int, db: Session = Depends(get_db)):
    query_deletar = db.query(Prestador).filter(Prestador.id == id)
    if query_deletar.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O prestador com id: {id} não existe"
        )
    query_deletar.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.PrestadorResponse)
def atualizar_prestador(update_dados: schemas.PrestadorBase, id: int, db: Session = Depends(get_db)):
    query_atualizar = db.query(Prestador).filter(Prestador.id == id)
    if query_atualizar.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"O prestador com id: {id} não existe"
        )
    query_atualizar.update(update_dados.dict(), synchronize_session=False)
    db.commit()
    return query_atualizar.first()