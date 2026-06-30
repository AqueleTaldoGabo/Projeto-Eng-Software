from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_db
from src import schemas
from src.entities.Cliente import Cliente

router = APIRouter(
    prefix='/clientes',
    tags=['Clientes']
)

@router.get('/', response_model=List[schemas.ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    return clientes

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ClienteResponse)
def criar_cliente(cliente_in: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # Valida se o email já existe
    email_existente = db.query(Cliente).filter(Cliente.email == cliente_in.email).first()
    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este e-mail já está cadastrado."
        )

    novo_cliente = Cliente(**cliente_in.dict())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@router.get('/{id}', response_model=schemas.ClienteResponse, status_code=status.HTTP_200_OK)
def buscar_cliente_por_id(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"O cliente com id: {id} não existe"
        )
    return cliente

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(id: int, db: Session = Depends(get_db)):
    query_deletar = db.query(Cliente).filter(Cliente.id == id)
    if query_deletar.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O cliente com id: {id} não existe"
        )
    query_deletar.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.ClienteResponse)
def atualizar_cliente(update_dados: schemas.ClienteBase, id: int, db: Session = Depends(get_db)):
    query_atualizar = db.query(Cliente).filter(Cliente.id == id)
    if query_atualizar.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"O cliente com id: {id} não existe"
        )
    query_atualizar.update(update_dados.dict(), synchronize_session=False)
    db.commit()
    return query_atualizar.first()